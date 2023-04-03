import json
import nltk
import pyttsx3
import random
import speech_recognition as sr

# Load the data from the JSON file
with open('patterns.json') as file:
    data = json.load(file)

# Initialize the NLTK tokenizer and stemmer
tokenizer = nltk.tokenize.TreebankWordTokenizer()
stemmer = nltk.stem.PorterStemmer()

# Initialize the pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Define the function to get a response to a user's message
def get_response(message):
    # Tokenize and stem the user's message
    tokens = tokenizer.tokenize(message.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Loop through the intents to find a match
    for intent in data['intents']:
        for pattern in intent['patterns'][engine.getProperty('voice')[0:2]]:
            # Tokenize and stem the pattern
            pattern_tokens = tokenizer.tokenize(pattern.lower())
            pattern_stemmed_tokens = [stemmer.stem(token) for token in pattern_tokens]

            # If the pattern matches the user's message, return a random response
            if set(stemmed_tokens) == set(pattern_stemmed_tokens):
                responses = intent['responses'][engine.getProperty('voice')[0:2]]
                return responses[random.randint(0, len(responses)-1)]

    # If no match was found, return a default response
    return "I'm sorry, I don't understand what you're asking."

# Initialize the wake word and sleep word
WAKE_WORD = 'sun'
SLEEP_WORD = 'boom'

# Define the function to listen for the wake word and start processing messages
def listen():
    # Initialize the speech recognition engine
    r = sr.Recognizer()

    # Start listening for the wake word
    with sr.Microphone() as source:
        print("Say something!")
        engine.say("Say something!")
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                if WAKE_WORD in text.lower():
                    print("Wake word detected!")
                    while True:
                        # Start listening for messages
                        audio = r.listen(source)
                        try:
                            text = r.recognize_google(audio)
                            print("You said:", text)
                            response = get_response(text)
                            print("Bot:", response)
                            engine.say(response)
                            engine.runAndWait()
                            if SLEEP_WORD in text.lower():
                                print("Sleep word detected!")
                                break
                        except sr.UnknownValueError:
                            print("Could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except sr.UnknownValueError:
                print("Could not understand audio")
                engine.say("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Start listening for the wake word and processing messages
listen()
