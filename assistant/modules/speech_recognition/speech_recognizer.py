import speech_recognition as sr
from google.cloud import dialogflow
import wave


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self, timeout):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout)
                text = self.recognizer.recognize_google(audio)
                print(text)
                file_path = "input.wav"
                with open(file_path, "wb") as f:
                    f.write(audio.get_wav_data())
                #print("Audio saved to {}".format(file_path))
                return file_path,text
        except sr.UnknownValueError:
            print("Unable to recognize speech. Please try again.")
        except sr.RequestError as e:
            print("Speech recognition request error: {}".format(e))
        return None,0



    def Speech_Text(self, project_id, session_id, audio_file_path, language_code):
        if audio_file_path is None:
            print("No audio file available. Speech recognition cannot proceed.")
            return None
        session_client = dialogflow.SessionsClient()
        audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        # Get the sample rate of the audio file
        with wave.open(audio_file_path, "rb") as audio_file:
            sample_rate_hertz = audio_file.getframerate()

        session = session_client.session_path(project_id, session_id)
        print("Session path: {}\n".format(session))

        with open(audio_file_path, "rb") as audio_file:
            input_audio = audio_file.read()

        audio_config = dialogflow.InputAudioConfig(
            audio_encoding=audio_encoding,
            language_code=language_code,
            sample_rate_hertz=sample_rate_hertz,
        )
        query_input = dialogflow.QueryInput(audio_config=audio_config)

        request = dialogflow.DetectIntentRequest(
            session=session,
            query_input=query_input,
            input_audio=input_audio,
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        return response.query_result.query_text
