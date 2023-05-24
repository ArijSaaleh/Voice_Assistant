import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            return audio

    def recognize_speech(self, audio):
        try:
            print("Recognizing speech...")
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service: {e}")
            return None
