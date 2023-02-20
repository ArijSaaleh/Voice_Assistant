import time
import random
import re
import spacy

# Load the Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Define wake word and sleep word
wake_word = "hey capri"
sleep_word = "goodbye"

# Define response patterns by tags
response_patterns = {
    "greetings": {
        "patterns": ["hello", "hi", "hey", "greetings"],
        "responses": ["Hello, how can I assist you?", "Hi there! How can I help you today?"]
    },
    "time": {
        "patterns": ["what time is it", "what's the time", "tell me the time"],
        "responses": ["It's currently " + time.strftime("%I:%M %p")]
    },
    "weather": {
        "patterns": ["what's the weather like", "what's the temperature", "is it hot outside"],
        "responses": ["The current temperature is " + str(random.randint(60, 100)) + " degrees Fahrenheit."]
    }
}

# Define function to match input to patterns and generate response
def generate_response(input_text):
    # Initialize response variable
    response = None
    
    # Check if input matches wake word or sleep word
    if input_text.lower() == wake_word:
        response = "Yes, how can I assist you?"
    elif input_text.lower() == sleep_word:
        response = "Goodbye!"
    else:
        # Iterate over response patterns
        for tag, pattern in response_patterns.items():
            # Iterate over patterns in the tag
            for p in pattern["patterns"]:
                # Match input to pattern using Spacy NLP
                match = re.search(p, input_text)
                if match:
                    # Generate a random response from responses in the tag
                    response = random.choice(pattern["responses"])
                    break
            if response:
                break
                
    # If no response is generated, return a default message
    if not response:
        response = "I'm sorry, I didn't understand your request."
    
    return response

# Define function to start voice assistant
def start_assistant():
    # Initialize voice recognition module
    # ...

    # Start listening for input
    while True:
        # Listen for input and convert to text
        input_text = ""  # Use voice recognition module to convert audio input to text

        # Check if input matches wake word or sleep word
        if input_text.lower() == wake_word or input_text.lower() == sleep_word:
            print(generate_response(input_text))
        else:
            # Use Spacy NLP to process input text
            input_doc = nlp(input_text)

            # Iterate over sentences in input
            for sentence in input_doc.sents:
                # Iterate over tokens in sentence
                for token in sentence:
                    # Check if token is a stop word or punctuation mark
                    if token.is_stop or token.is_punct:
                        continue

                    # Generate response for each topic with a pattern that matches the token
                    for tag, pattern in response_patterns.items():
                        for p in pattern["patterns"]:
                            if p in token.text.lower():
                                print(generate_response(input_text))
                                break

# Start the voice assistant
start_assistant()
