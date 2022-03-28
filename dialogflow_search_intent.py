import logging
from google.cloud import dialogflow


logger = logging.getLogger(__file__)


def get_answer_from_dialogflow(
    project_id,
    session_id,
    texts,
    language_code='ru'
):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    logger.debug("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    logger.debug(f"Query text: {response.query_result.query_text}")
    logger.debug(
        f"Detected intent: {response.query_result.intent.display_name}"
        f"(confidence: {response.query_result.intent_detection_confidence})"

    )
    logger.debug(f"Fulfillment text: {response.query_result.fulfillment_text}")

    return response
