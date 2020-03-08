import speech_recognition as sr
import pyttsx3

class Speech:
    TEXT_BEGIN_ASK = "Should I begin collecting papers?"
    TEXT_NOT_UNDERSTAND = "Could not understand what you said."

    def __init__(self):
        self.engine = pyttsx3.init()

    def sayWait(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class Recogniser:
    def __init__(self, speech):
        self.r = sr.Recognizer()
        self.__speech = speech
    
    def recognize_sentence_loop(self):
        count = 0
        with sr.Microphone() as source:
            while True:
                #Take some time to adjust for noise
                if count <= 0:
                    print("Adjusting for noise...")
                    #self.r.adjust_for_ambient_noise(source, duration = 2)
                    count = 5
                
                print("Listening...")
                audio = self.r.record(source, duration = 3)#r.listen(source)
                
                try:
                    text = self.r.recognize_google(audio)
                    print("Said", text)
                except:
                    speaker.sayWait(Speech.TEXT_NOT_UNDERSTAND)
                    print("Not understood??")
                    
                count -= 1 

speaker = Speech()
voice_rec = Recogniser(speaker)

speaker.sayWait(Speech.TEXT_BEGIN_ASK)
voice_rec.recognize_sentence_loop()

'''
class speech:
    def__init__(self):
        engine=pyttsx3.init()
        engine.say("Should I begin collecting papers : ")
        engine.runAndWait()

        engine=pyttsx3.init()
        r=sr.Recognizer()
        new_rate=0.99

    while True: 
        try:
            
                with sr.Microphone() as source: 
                    audio=r.record(source, duration = 3)#r.listen(source)
                    text=r.recognize_sphinx(audio)
                print("You said : {}".format(text))
                if(text=="begin"):
                    engine.say("Paper collection beginning")
                    engine.runAndWait()
                    break
                elif(text=="exit"):
                    engine.say("Activating sleep mode")
                    engine.runAndWait()
                    break
                elif(text=="stop"):
                    engine.say("Paper collection stopped")
                    engine.runAndWait()
                    break
                else:
                
                    engine.setProperty('rate',new_rate)
                    engine.say("Say. a. valid. command.? say either Begin., STOP.. OR.. Exit..",)
                    engine.runAndWait()
                    
                        
            
        except sr.UnknownValueError as e:
            engine.say("Could not understand what you said")
            engine.runAndWait()
            print(e)        
        except sr.RequestError as e:
                    engine.say("Could not understand what you said")
                    engine.runAndWait() 
                    print("Sphinx error; {0}".format(e))  

                
                    
    engine.runAndWait()



obj1=ease()
obj2=ease2()
'''