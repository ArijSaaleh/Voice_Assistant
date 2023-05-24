from .modules.speech_recognition import speech_recognizer
from .modules.NLP import nlp_processor
from .modules.action_handler import action_handler
from .modules.text_to_speech import tts_converter

class VoiceAssistant:
    def __init__(self):
        self.speech_recognizer = speech_recognizer.SpeechRecognizer()
        self.nlp_processor = nlp_processor.NLPProcessor()
        self.action_handler = action_handler.ActionHandler()
        self.text_to_speech_converter = tts_converter.TextToSpeechConverter()

    def run(self):
        while True:
            # Listen for user input
            audio = self.speech_recognizer.listen()

            # Process user input
            text = self.speech_recognizer.recognize_speech(audio)
            intent, entities = self.nlp_processor.process_input(text)

            # Handle action based on intent and entities
            response = self.action_handler.handle_action(intent, entities)

            # Convert response to speech and speak
            speech = self.text_to_speech_converter.convert_text(response)
            self.text_to_speech_converter.speak(speech)
