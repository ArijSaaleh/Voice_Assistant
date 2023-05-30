from google.cloud import dialogflow

class NLPProcessor:
    def __init__(self):
        self.session_client = dialogflow.SessionsClient()

    def process_input(self, text, project_id, session_id, language_code):
        session_path = self.session_client.session_path(project_id, session_id)
        print("Session path: {}\n".format(session_path))

        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        
        output_audio_config = dialogflow.OutputAudioConfig(
            audio_encoding=dialogflow.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16
        )

        request = dialogflow.DetectIntentRequest(
            session=session_path,
            query_input=query_input,
            output_audio_config=output_audio_config,
        )
        
        response = self.session_client.detect_intent(request=request)

        intent = response.query_result.intent.display_name
        confidence = response.query_result.intent_detection_confidence
        fulfillment_text = response.query_result.fulfillment_text

        return response, fulfillment_text, confidence
