import dialogflow

class NLPProcessor:
    def __init__(self):
        self.project_id = "your-dialogflow-project-id"
        self.session_client = dialogflow.SessionsClient()

    def process_input(self, text):
        session = self.session_client.session_path(self.project_id, "unique-session-id")
        query_input = dialogflow.types.QueryInput(text=dialogflow.types.TextInput(text=text))
        response = self.session_client.detect_intent(session=session, query_input=query_input)

        intent = response.query_result.intent.display_name
        entities = [(entity.name, entity.value) for entity in response.query_result.parameters.fields.values()]

        return intent, entities
