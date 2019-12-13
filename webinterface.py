from flask import Flask, render_template, Response, request
from cv2 import imencode, rectangle, resize, FONT_HERSHEY_SIMPLEX, LINE_AA, putText
from threading import Thread
from motors import MotorController
from time import time

appThread = None
claw = None
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def run():
    global app
    app.run(host='0.0.0.0', threaded=True)

def begin():
    global appThread
    appThread = Thread(target = run)
    appThread.start()
    return appThread

def setClawObj(cl):
    global claw
    claw = cl

#================== Flask app ==================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ioState')
def gpioFn():
    global ioc, claw
    if 'motor1Speed' in request.args.keys():
        try:
            mtrSpeed = int(request.args['motor1Speed'])
            MotorController.customLeftMotor(mtrSpeed)
            
        except ValueError:
            print("Bad input received:", request.args['motor1Speed'])
    
    if 'motor2Speed' in request.args.keys():
        try:
            mtrSpeed = int(request.args['motor2Speed'])
            MotorController.customRightMotor(mtrSpeed)
            
        except ValueError:
            print("Bad input received:", request.args['motor2Speed'])
    
    if 'action' in request.args.keys():
        act = request.args['action']
        
        if claw is not None:
            if act == "arm_raise":
                claw.armRestingPos()
            elif act == "arm_lower":
                claw.armReach()
            elif act == "claw_toggle":
                if claw.claw_state == "open":
                    claw.closeClaw()
                else:
                    claw.openClaw()
    if "arm_height" in request.args.keys():
        try:
            claw.sweepServo('height', int(request.args['arm_height']))
        except:
            pass
    
    if "arm_linear" in request.args.keys():
        try:
            claw.sweepServo('linear', int(request.args['arm_linear']))
        except:
            pass
    
    if "arm_percent" in request.args.keys():
        try:
            claw.armAt(int(request.args['arm_percent']) / 100.0)
        except:
            pass
            
    #if 'togglemode' in request.args.keys():
    #    if mode == 'auto':
    #        mode = 'manual'
    #    else:
    #        mode = 'auto'
            
    return ''
