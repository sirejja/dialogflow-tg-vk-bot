import logging
import os
import vk_api as vk
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow


load_dotenv()
VK_TOKEN = os.environ['VK_TOKEN']
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']


logger = logging.getLogger(__name__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
