import pyttsx3


class TextToSpeechConverter:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        # Set the speech rate (words per minute)
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 0.8)  # Set the volume (0.0 to 1.0)
        self.engine.say(text)  # Convert text to speech
        self.engine.runAndWait()
