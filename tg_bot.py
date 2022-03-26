import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from utils import get_bot_handler


logger = logging.getLogger(__file__)


load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
TG_LOGS_TOKEN = os.environ['TG_LOGS_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']


def detect_intent_texts(project_id, session_id, texts, language_code='ru'):
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


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!"
    )


def typical_question(
    update: Update,
    context: CallbackContext
):

    dialogflow_intent_response = detect_intent_texts(
        project_id=DIALOGFLOW_PROJECT_ID,
        session_id=update.effective_chat.id,
        texts=update.message.text
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogflow_intent_response.query_result.fulfillment_text
    )


def main():

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(
        get_bot_handler(
            Bot(token=TG_LOGS_TOKEN),
            TG_CHAT_ID
        )
    )

    logger.info('Starting Game of Verbs TG bot')

    try:
        updater = Updater(token=TG_TOKEN)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        typical_question_handler = MessageHandler(
            Filters.text & (~Filters.command),
            typical_question
        )
        dispatcher.add_handler(typical_question_handler)

        updater.start_polling()
    except ConnectionError:
        logger.exception('ConnectionError messages bot')
    except Exception as e:
        logger.exception('Unexpected exception has occured')
        raise e



if __name__ == '__main__':
    main()
