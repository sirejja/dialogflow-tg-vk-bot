import logging
import os
import vk_api as vk
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Bot

from tg_bot import detect_intent_texts
from utils import get_bot_handler

logger = logging.getLogger(__file__)


def typical_question(event, vk_api, dialog_flow_project_id):

    random_id = random.randint(1, 1000)

    dialogflow_intent_response = detect_intent_texts(
        project_id=dialog_flow_project_id,
        session_id=random_id,
        texts=event.text
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_intent_response,
        random_id=random_id
    )


if __name__ == "__main__":
    load_dotenv()
    VK_TOKEN = os.environ['VK_TOKEN']
    DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
    TG_LOGS_TOKEN = os.environ['TG_LOGS_TOKEN']
    TG_CHAT_ID = os.environ['TG_CHAT_ID']

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(
        get_bot_handler(
            Bot(token=TG_LOGS_TOKEN),
            TG_CHAT_ID
        )
    )
    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            typical_question(event, vk_api, DIALOGFLOW_PROJECT_ID)
