import json
import requests
import speech_recognition as sr
import spacy
import pyttsx3

# load the English and French language models from spacy
nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')

# initialize text-to-speech engine
engine = pyttsx3.init()

# define a function to speak the response
def say(text):
    engine.say(text)
    engine.runAndWait()

# define a function to get the weather for a given city
def get_weather(city, lang):
    API_KEY = "YOUR_API_KEY_HERE" # replace with your own API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={lang}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        say(f"In {city}, it is currently {temp} degrees Celsius and {weather}")
    else:
        say("I'm sorry, I couldn't get the weather for that city. Please try again later.")

# load the pattern file
with open('patterns.json') as f:
    patterns = json.load(f)

# define a function to process the user's input
def process_input(text, lang):
    doc = nlp_en(text) if lang == "en" else nlp_fr(text)
    for tag, patterns_and_responses in patterns[lang].items():
        for pattern, responses in patterns_and_responses.items():
            pattern_doc = nlp_en(pattern) if lang == "en" else nlp_fr(pattern)
            if pattern_doc.similarity(doc) > 0.8:
                response = responses[0] # get the first response
                if "{weather_city}" in response:
                    # get the weather for the city in the user's input
                    for token in doc:
                        if token.ent_type_ == "GPE":
                            city = token.text
                            get_weather(city, lang)
                            return
                say(response)
                return
    say("I'm sorry, I didn't understand what you said. Please try again.")

# initialize the speech recognition engine
r = sr.Recognizer()

# define the wake word and sleep word
WAKE_WORD = "hey assistant"
SLEEP_WORD = "goodbye assistant"

# define a function to listen for the wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text == WAKE_WORD:
                return True
        except:
            pass
    return False

# define a function to listen for the user's input
def listen_for_input():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""

# define a function to listen for the sleep word
def listen_for_sleep_word():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""