import argparse
import os
import logging
import json

from dotenv import load_dotenv
from google.cloud import dialogflow


load_dotenv()
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']


logger = logging.getLogger(__name__)


def create_intent(
    project_id,
    display_name: str,
    training_phrases_parts: list,
    message_texts: list
):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.info(f"Intent created: {response}")


def main():
    parser = argparse.ArgumentParser(
        description='Обучение dialogflow agent'
    )
    parser.add_argument('-p', '--path', help='Название обучающего файла')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    with open(args.path, "r", encoding='utf-8') as file:
        questions = json.load(file)

        for question, question_body in questions.items():

            create_intent(
                project_id=DIALOGFLOW_PROJECT_ID,
                display_name=question,
                training_phrases_parts=question_body['questions'],
                message_texts=[question_body['answer']]
            )


if __name__ == '__main__':
    main()
