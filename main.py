from assistant.modules.NLP.nlp_processor import NLPProcessor
from assistant.modules.text_to_speech.tts_converter import TextToSpeechConverter
from assistant.modules.speech_recognition.speech_recognizer import SpeechRecognizer
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
# KEY VARIABLE FOR GCP-DF
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_key.json"
project_id = os.getenv("PROJECT_KEY")
session_id = os.getenv("SESS_ID")
# Create an instance of NLPProcessor
nlp_processor = NLPProcessor()
# Create an instance of TextToSpeechConverter
tts_converter = TextToSpeechConverter()
# Create an instance of SpeechRecognizer
stt_converter = SpeechRecognizer()
language_code = "en"
while True:
    audio_file_path, text = stt_converter.listen(9)

    texts = text
    response, fulfilment_text, confidence = nlp_processor.process_input(
        texts, project_id, session_id, language_code
    )
    if response is not None and response.query_result is not None:
        fulfilment_text = response.query_result.fulfillment_text
        confidence = response.query_result.intent_detection_confidence
        print("Fulfillment text: {}".format(fulfilment_text))
        print("Confidence: {}".format(confidence))#hhhh
        tts_converter.speak(response)
        texts=""
    else:
        print("No valid response received from Dialogflow.")
