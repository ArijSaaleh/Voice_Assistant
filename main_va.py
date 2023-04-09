import speech_recognition as sr
import pyttsx3
import json
import random
import nltk
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re  # regular-expression
import fasttext

model = fasttext.load_model('lid.176.bin')
nltk.download('stopwords')
nltk.download('wordnet')
# Load the question-response pairs from the json file
with open('patterns.json', 'r') as f:
    data = json.load(f)

# Initialize the wake word and sleep word
WAKE_WORD = 'sun'
SLEEP_WORD = 'boom'

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 150)  # Change the speed
engine.setProperty('volume', 1)  # Change the volume


# Define a function to convert text to speech
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # handle the error gracefully
        print(f"Error speaking: {{str(e)}}")
    finally:
        # ensure the engine is always stopped
        engine.stop()

# Define a function to tokenize and stem the user input
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(sentence,lang):
    # Normalize the sentence : convert to lowercase and remove any punctuation or special characters.
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w\s]', '', str(sentence))

    # Remove stop words based on language: the, a, an, in, on at ..
    if lang == 'en':
        tokens = sentence.split()
        tokens = [token for token in tokens if token not in stop_words]
        # Lemmatize tokens :  lemmatization instead of stemming: Lemmatization is a process of reducing words to their base form, which is more accurate than stemming(Stemming removes the suffix of a word to get its root form).
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    elif lang == 'fr':
        # Add French stopwords
        stop_words_fr = set(stopwords.words('french'))
        tokens = sentence.split()
        tokens = [token for token in tokens if token not in stop_words_fr]
        tokens = [lemmatizer.lemmatize(token, 'v') for token in tokens]  # lemmatize verbs only
    else:
        # For unsupported languages, just split the sentence into tokens
        tokens = sentence.split()
    
    return tokens

# Define a function to get intent from the json file
def get_intent(user_input, intents, language):
    max_score = 0
    matched_intent = None
    try:
        for intent in intents:
            if 'patterns' in intent and language in intent['patterns']:
                for pattern in intent['patterns'][language]:
                    score = fuzz.partial_ratio(str(user_input).lower(), pattern.lower())
                    if score > max_score:
                        max_score = score
                        matched_intent = intent
        # Calculate confidence score
        confidence = max_score / 100
        print("Intent : ",)
        # If confidence is low, trigger fallback intent
        if confidence < 0.5:
            if(language=="fr"):
                matched_intent = {'tag': 'fallback', 'response': "Désolé, Je vous comprends pas. Reformule s'il vous plait?"}
            else:
                matched_intent = {'tag': 'fallback', 'response': "Sorry, I didn't understand that. Can you please rephrase?"}
        
        return matched_intent, confidence
    except Exception as e:
        print(f'Error intent: {str(e)}')
        return {'tag': 'error', 'response': 'Oops, something went wrong! Please try again later.'}, 0
# Define a function to get a response to a user input
def get_response(user_input,language):
    try:
        
        # Load intents for the detected language
        with open(f'patterns.json', 'r') as file:
            intents = json.load(file)['intents']

        # Preprocess user input
        tokens = preprocess(user_input,language)
        
        # Get the intent with the highest confidence score
        matched_intent, confidence = get_intent(tokens, intents, language)
        print("respooonsee  ", matched_intent)
        print("fi wost response", matched_intent,"conf: ",confidence)
        
        # Select a random response from the matched intent
        response = random.choice(matched_intent['responses'][language])

        # Speak the response
        speak(response)

        return response,confidence
    except Exception as e:
        print(f"Error response: {e}")
        return "Sorry, something went wrong. Can you please try again?", 0.0


# Start the voice assistant
while True:
    #user_input = input('You: ')
    user_input= recognize_speech()
    if user_input:
        language = model.predict(user_input)[0][0][-2:]
        print("Lang: "+ language)
        print("You said : "+ user_input)
        # Preprocess user input
        preprocessed_input = preprocess(user_input,language)
        with open(f'patterns.json', 'r') as file:
            intents = json.load(file)['intents']
        # Get intent and confidence score
        intent, confidence = get_intent(preprocessed_input, intents,language)
        #print("houni mainnn :", intent)
        print("confiiiiii : ",confidence)
        # Get response for the intent
        response = get_response(user_input,language)
        # Handle low confidence score
        if confidence < 0.5:
            #print(len(intents)-1)
            print("Bot:", intents[len(intents)-1]["responses"][language]) #response = get_response(fallback_intent, language)
            print("fallbackkkkk")
            continue
        # Handle missing response
        if response is None:
            print("Bot: I'm sorry, I don't know how to respond to that.")
            speak("Bot: I'm sorry, I don't know how to respond to that.")
            continue
        # Print the response
        print("Bot:", response)