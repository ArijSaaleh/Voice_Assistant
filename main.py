from assistant.modules.NLP.nlp_processor import NLPProcessor
from assistant.modules.text_to_speech.tts_converter import TextToSpeechConverter
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()
# KEY VARIABLE FOR GCP-DF
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='private_key.json'
project_id=os.getenv("PROJECT_KEY") 
session_id=os.getenv("SESS_ID")

texts=["who are you"]
language_code="en"
# Create an instance of NLPProcessor
nlp_processor = NLPProcessor()
# Create an instance of TextToSpeechConverter
tts_converter = TextToSpeechConverter()

response, fulfilment_text, confidence = nlp_processor.process_input(texts[0], project_id, session_id, language_code)
print(fulfilment_text)
# Call the speak method with the response
tts_converter.speak(response)
