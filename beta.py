import speech_recognition as sr
import pyttsx3
import re
import time

# Define a function that reads a pattern file and returns a dictionary of patterns and responses grouped by tags
def read_pattern_file(pattern_file):
    with open(pattern_file) as f:
        pattern_dict = {}
        current_tag = None
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_tag = line[1:-1]
                pattern_dict[current_tag] = []
            elif current_tag is not None and line:
                pattern, response = line.split(",")
                pattern_dict[current_tag].append((re.compile(pattern.strip()), response.strip()))
    return pattern_dict

# Define a function that matches user input to patterns in the pattern dictionary and returns a response
def respond(input_text, pattern_dict):
    for tag, patterns in pattern_dict.items():
        for pattern, response in patterns:
            if pattern.search(input_text):
                return response
    return "I'm sorry, I didn't understand your question."

# Set up the speech-to-text and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('language', "en_GP")
# Load the pattern file and create the pattern dictionary
pattern_file = "patterns.txt"
pattern_dict = read_pattern_file(pattern_file)

# Define the wake word and sleep word
wake_word = "hey assistant"
sleep_word = "goodbye assistant"

# Start the voice assistant
is_awake = False
while True:
    with sr.Microphone() as source:
        if not is_awake:
            print("Waiting for wake word...")
        audio = r.listen(source)
    try:
        start_time = time.monotonic()
        user_input = r.recognize_google(audio)
        print("You said: " + user_input)
        if not is_awake:
            if re.search(wake_word, user_input):
                is_awake = True
                response = "Hello, how can I help you?"
                print(response)
                engine.say(response)
                engine.runAndWait()
        elif re.search(sleep_word, user_input):
            is_awake = False
            response = "Goodbye, have a nice day!"
            print(response)
            engine.say(response)
            engine.runAndWait()
        else:
            response = respond(user_input, pattern_dict)
            print(response)
            engine.say(response)
            engine.runAndWait()
        end_time = time.monotonic()
        print("Response time: {:.2f} seconds".format(end_time - start_time))
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        engine.say("Sorry, I could not understand what you said.")
        engine.runAndWait()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Sorry, I could not understand what you said.")
        engine.runAndWait()
