import speech_recognition as sr
import pyttsx3
import json
import random
import nltk
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import re  # regular-expression
nltk.download('stopwords')
# Load the question-response pairs from the json file
with open('patterns.json', 'r') as f:
    data = json.load(f)

# Initialize the wake word and sleep word
WAKE_WORD = 'sun'
SLEEP_WORD = 'boom'

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)  # Change the speed
engine.setProperty('volume', 1)  # Change the volume

# Define a function to recognize speech
def recognize_speech():
    r = sr.Recognizer()
    # Check if the microphone is available
    if not sr.Microphone.list_microphone_names():
        return "No microphone found. Please connect a microphone and try again."
    # Adjust for ambient noise and listen to the audio input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Can you please repeat?"
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service. Please try again later."
        except sr.WaitTimeoutError:
            return "Sorry, I didn't hear anything. Please try again."

# Define a function to convert text to speech
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait(timeout=10)
    except Exception as e:
        # handle the error gracefully
        print(f"Error speaking: {str(e)}")
    finally:
        # ensure the engine is always stopped
        engine.stop()

# Define a function to tokenize and stem the user input
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(sentence,lang):
    # Detect the language of the sentence
    #lang = TextBlob(str(sentence)).detect_language()
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
def get_intent(user_input, intents,language):
    max_score = 0
    matched_intent = None
    
    try:
        for intent in intents:
            if language in intent['patterns']:
                for pattern in intent['patterns'][language]:
                    score = fuzz.partial_ratio(user_input.lower(), pattern.lower())
                    if score > max_score:
                        max_score = score
                        matched_intent = intent
        # Calculate confidence score
        confidence = max_score / 100
        # If confidence is low, trigger fallback intent
        if confidence < 0.5:
            if(language=="fr"):
                matched_intent = {'tag': 'fallback', 'response': "Désolé, Je vous comprends pas. Reformule s'il vous plait?"}
            else:
                matched_intent = {'tag': 'fallback', 'response': "Sorry, I didn't understand that. Can you please rephrase?"}
        
        return matched_intent, confidence
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'tag': 'error', 'response': 'Oops, something went wrong! Please try again later.'}, 0
# Define a function to get a response to a user input
def get_response(user_input,language):
    # Check if user input is empty
    if not user_input:
        speak("Sorry, I didn't get that. Can you please repeat?")
        return "Sorry, I didn't get that. Can you please repeat?", 0.0
    try:

        # Detect user's language
        #language = TextBlob(user_input).detect_language()
        
        # Load intents for the detected language
        with open(f'patterns.json', 'r') as file:
            intents = json.load(file)['intents']
        
        # Preprocess user input
        tokens = preprocess(user_input)
        
        # Get the intent with the highest confidence score
        matched_intent, confidence = get_intent(tokens, intents)
        
        # Select a random response from the matched intent
        response = random.choice(matched_intent['responses'][language])

        # Speak the response
        speak(response)

        return response,confidence
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong. Can you please try again?", 0.0


# Start the voice assistant
while True:
    user_input = input('You: ')
    language=''
    print("hani houni : "+ language)
    # Preprocess user input
    preprocessed_input = preprocess(user_input,language)
    with open(f'patterns.json', 'r') as file:
        intents = json.load(file)['intents']
    # Get intent and confidence score
    intent, confidence = get_intent(str(preprocessed_input), intents,language)
     # Handle low confidence score
    if confidence < 0.5:
        #print(len(intents)-1)
        print("Bot:", intents[len(intents)-1]["responses"]) #response = get_response(fallback_intent, language)
        continue
    # Get response for the intent
    response = get_response(user_input,language)
    # Handle missing response
    if response is None:
        print("Bot: I'm sorry, I don't know how to respond to that.")
        speak("Bot: I'm sorry, I don't know how to respond to that.")
        continue
    # Print the response
    print("Bot:", response)