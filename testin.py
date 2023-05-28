# Main Libraries
import speech_recognition as sr
import pyttsx3
import json
import random
import time
import re  # regular expression
import fasttext
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz  # used for string matching
from elevenlabs import generate, stream, voices

# stopwords (a and that there ..)
# nltk.download('stopwords')
# nltk.download('wordnet')

# model of language detection
model = fasttext.load_model('lid.176.bin')

# Loading patterns & responses from the json file
with open('patterns.json', 'r') as f:
    data = json.load(f)
# loading intents from the json data
intents = data['intents']
# Initializing the wake up and sleep words
wake_up = 'sun'
sleep = 'cease all motor functions'

# Function to speak (convert text to speech)
def speak(text):
    audio_stream = generate(
        text=text,
        stream=True)
    stream(audio_stream)

# Function to recognize the speech
def recognizeSpeech():
    r = sr.Recognizer()
    # testing the microphone availability
    microphone_names = sr.Microphone.list_microphone_names()
    if not microphone_names:
        return "No mic found, plz connect a mic"
    # adjust ambient noise and listen to audio input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 600
        """
        # Prompt the user to speak
        print("Hello there how can I help you?")
        speak("Hello there how can I help you?")
        time.sleep(3)  # Wait for 2 seconds to give user time to speak"""
        try:
            audio = r.listen(source)
            user_input = r.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            print("mafhemt chay")
            return None
        except sr.RequestError:
            print("No internet for audio")
            return None
        except sr.WaitTimeoutError:
            print("Too long to speak")
            return None
# Function to preprocess the user input


def preprocess(sentence, lang):
    # tokenize and stem the user input
    stop_words = set(stopwords.words('english'))
    stop_words_fr = set(stopwords.words('french'))
    lemmatizer = WordNetLemmatizer()
    # Normalize the sentence : convert to lowercase and remove any punctuation or special characters.
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w\s]', '', str(sentence))
    # Remove stop words based on language
    if lang == 'en':
        tokens = sentence.split()
        tokens = [token for token in tokens if token not in stop_words]
        """ Lemmatize tokens :  lemmatization instead of 
        stemming: Lemmatization is a process of 
        reducing words to their base form, 
        which is more accurate than stemming(
        stemming removes the suffix of a word to get its root form)."""
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    elif lang == 'fr':
        tokens = sentence.split()
        tokens = [token for token in tokens if token not in stop_words_fr]
        tokens = [lemmatizer.lemmatize(token, 'v')
                  for token in tokens]  # lemmatize verbs only
    else:
        # For unsupported languages, just split the sentence into tokens
        tokens = sentence.split()
    return tokens
# Function to search for the intent in the jsonfile


def get_intent(user_input, intents, language):
    best_match = None
    score = 0
    try:
        for intent in intents:
            if 'patterns' in intent and language in intent['patterns']:
                for pattern in intent['patterns'][language]:
                    current_score = fuzz.partial_ratio(
                        str(user_input).lower(), str(pattern).lower())
                    print("ssss ", current_score)
                    if current_score > score:
                        score = current_score
                        best_match = intent
                        print("hhhh : ", best_match, score)
        return best_match, score
    except Exception as e:
        print(f'Error intent: {str(e)}')
        return "error getting the intent", 0
# Function to get the response based on the intent


def get_response(intent, language):
    if intent:

        try:
            # select a random response
            response = random.choice(intent['responses'][language])
            # speak the response
            print("R gR: ", response)
            speak(response)
            return response, confidence
        except Exception as e:
            print(f"Error response: {e}")
            return "error getting response", 0
    else:
        speak("Sorry")
        print("sorry")


# Main Loop
while True:
    user_intent = recognizeSpeech()
    if user_intent:
        print("you said", user_intent)
        language = model.predict(user_intent)[0][0][-2:]
        # Preprocess user input
        preprocessed_input = preprocess(user_intent, language)
        # get intent
        intent, confidence = get_intent(preprocessed_input, intents, language)
        print("Main intent: ", intent, confidence)
        # get response
        response, confidence = get_response(intent, language)
        print("main Response: ", response, confidence)
        # Handle no response found
        if response is None:
            print("Sorry I don't know how to response.")
            speak("Sorry I don't know how to response.")
            continue