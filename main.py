import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', "Persian+English-US")  # Select the first available voice
    engine.setProperty('rate', 120)  # Set the speech rate to 150 words per minute
    engine.setProperty('volume', 0.8)  # Adjust the speech volume
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"You said: {query}")
        return query
    except Exception as e:
        print("Sorry, I couldn't understand. Can you please repeat that?")
        return ""

def process_query(query):
    if "hello" in query:
        speak("Hello! How can I assist you today?")
    elif "time" in query:
        # You can implement the logic to get the current time here
        speak("The current time is 9:00 AM.")
    elif "weather" in query:
        # You can implement the logic to fetch the weather information here
        speak("The weather today is sunny.")
    else:
        speak("I'm sorry, I don't have information about that.")

def run_jarvis():
    speak("Hello! I am Jarvis, your virtual assistant.")
    while True:
        query = listen().lower()
        if "exit" in query:
            speak("Goodbye!")
            break
        process_query(query)

if __name__ == '__main__':
    run_jarvis()
   #pass
