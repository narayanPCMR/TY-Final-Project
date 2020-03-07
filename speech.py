import pyttsx3

class Speech:
    BEGUN ="Paper collection begun"
    AUTOON="automatic mode activated"
    AUTOOFF="automatic mode disabled"
    ON="powered on" 
    OFF="Shutting down"
    Restart="Manual Reset Successful"

    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    s=Speech()
    s.speak(Speech.BEGUN)
    s.speak(Speech.AUTOON)
    s.speak(Speech.AUTOOFF)
    s.speak(Speech.ON)
    s.speak(Speech.OFF)
    
