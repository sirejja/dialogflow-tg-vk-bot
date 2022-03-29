import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_search_intent import get_answer_from_dialogflow
from setup_logger import setup_logger

logger = logging.getLogger(__file__)


def process_message_vk(event, vk_api, dialog_flow_project_id):

    dialogflow_intent_response = get_answer_from_dialogflow(
        project_id=dialog_flow_project_id,
        session_id=f'vk-{event.user_id}',
        texts=event.text
    )

    if dialogflow_intent_response.query_result.intent.is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_intent_response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


def main():
    load_dotenv()
    setup_logger(os.environ['TG_LOGS_TOKEN'], os.environ['TG_CHAT_ID'])

    logger.info('Starting Game of Verbs VK bot')

    try:
        vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                process_message_vk(
                    event,
                    vk_api,
                    os.environ['DIALOGFLOW_PROJECT_ID']
                )

    except ConnectionError:
        logger.exception('ConnectionError messages bot')
    except Exception as e:
        logger.exception('Unexpected exception has occured')
        raise e


if __name__ == "__main__":
    main()
