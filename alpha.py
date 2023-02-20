import json
import random
import spacy

# Load the English and French language models
nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

# Load the pattern file
with open("pattern_file.json", "r") as f:
    patterns = json.load(f)

def detect_language(text):
    """
    Detect the language of the given text using spaCy's language detection pipeline.
    Returns "en" if English is detected, "fr" if French is detected, and None if the language is unknown.
    """
    doc = nlp_en(text)
    if doc._.language["language"] == "en":
        return "en"
    
    doc = nlp_fr(text)
    if doc._.language["language"] == "fr":
        return "fr"
    
    return None

def get_response(command):
    """
    Return a response based on the given command, using the appropriate set of patterns and responses
    based on the detected language.
    """
    lang = detect_language(command)
    
    if lang == "en":
        patterns_for_lang = patterns["english"]
    elif lang == "fr":
        patterns_for_lang = patterns["french"]
    else:
        return "I'm sorry, I don't understand."
    
    for topic in patterns_for_lang:
        for pattern in topic["patterns"]:
            if pattern in command:
                return random.choice(topic["responses"])
    
    return "I'm sorry, I don't understand."

# Example usage
while True:
    command = input("Speak a command: ")
    if command.lower() == "bye":
        break
    response = get_response(command)
    print(response)
