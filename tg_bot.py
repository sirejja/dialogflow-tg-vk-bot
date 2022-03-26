import logging
import os
from dotenv import load_dotenv

from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from google.cloud import dialogflow


load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']


logger = logging.getLogger(__name__)


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

    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!"
    )


def echo(update: Update, context: CallbackContext):

    dialogflow_intent_response = detect_intent_texts(
        project_id=DIALOGFLOW_PROJECT_ID,
        session_id=update.effective_chat.id,
        texts=update.message.text
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogflow_intent_response
    )


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    updater = Updater(token=TG_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
