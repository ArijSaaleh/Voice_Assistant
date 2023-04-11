import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
load_dotenv()

session_client = dialogflow.SessionsClient(credentials=credentials)
session = session_client.session_path(project_id, session_id)

text_input = dialogflow.types.TextInput(text=user_input, language_code=language)
query_input = dialogflow.types.QueryInput(text=text_input)
response = session_client.detect_intent(session=session, query_input=query_input)
intent = response.query_result.intent.display_name
parameters = response.query_result.parameters.fields
