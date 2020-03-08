from flask import Flask, render_template, Response, request
from cv2 import imencode, rectangle, resize, FONT_HERSHEY_SIMPLEX, LINE_AA, putText
from threading import Thread
from motors import MotorController
from time import time
from utils import Utils
from speech import Speech

appThread = None
claw = None
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

flag=1
speech =Speech()

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

def toggleMode():
    if Utils.mode == 'auto':
        speech.speak(speech.AUTOOFF)
        Utils.mode = 'manual'
    else:
        speech.speak(speech.AUTOON)
        Utils.mode = 'auto'
        Utils.pickupPhase = 0
    
    print("Mode changed to {}".format(Utils.mode))

#================== Flask app ==================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ioState')
def gpioFn():
    global ioc, claw, flag
    if 'motor1Speed' in request.args.keys():
        try:
            mtrSpeed = float(request.args['motor1Speed'])
            MotorController.customLeftMotor(mtrSpeed)
            
        except ValueError:
            print("Bad input received:", request.args['motor1Speed'])
    
    if 'motor2Speed' in request.args.keys():
        try:
            mtrSpeed = float(request.args['motor2Speed'])
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
            elif act == "arm_rotate":
                if flag==1:
                    claw.rotateClawBack()
                    flag=0
                else:
                    claw.rotateClawFront()
                    flag=1
                    
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
            
    if 'togglemode' in request.args.keys():
        toggleMode()
        return Utils.mode

    #if 'arm_rotate' in request.args.keys():
        
            
    return ''
