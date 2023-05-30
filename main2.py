from playsound import playsound
from google.cloud import dialogflow
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='assistant/private_key.json'
project_id="gpa-agent-uedj"
session_id="me"
texts=["ESPRIT"]
# [START dialogflow_detect_intent_with_texttospeech_response]
def detect_intent_with_texttospeech_response(
    project_id, session_id, texts, language_code
):
    """Returns the result of detect intent with texts as inputs and includes
    the response in an audio format.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        # Set the query parameters with sentiment analysis
        output_audio_config = dialogflow.OutputAudioConfig(
            audio_encoding=dialogflow.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16
        )

        request = dialogflow.DetectIntentRequest(
            session=session_path,
            query_input=query_input,
            output_audio_config=output_audio_config,
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        # The response's audio_content is binary.
        #playsound(response.output_audio)
        with open("output.wav", "wb") as out:
            out.write(response.output_audio)
            print('Audio content written to file "output.wav"')
            playsound("output.wav")
            print("ok")
detect_intent_with_texttospeech_response(project_id,session_id, texts, "en")