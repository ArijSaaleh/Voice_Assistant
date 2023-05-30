from playsound import playsound

class TextToSpeechConverter:
    def __init__(self):
        pass
        
    def speak(self, response):
        output_file = "output.wav"
        
        try:
            with open(output_file, "wb") as out:
                out.write(response.output_audio)
                print(f'Audio content written to file "{output_file}"')
            
            playsound(output_file)
            print("Playback completed.")
        except Exception as e:
            print(f"An error occurred during playback: {str(e)}")