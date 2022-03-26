# Conversational Bot for Telegram and VK Groups

## Features:
* Bot for Telegram
* Bot for VK Group
* Telegram bot for logging
* Support quering Dealogfloa API
* Script for training DialogFlow agent AI


## Google Cloud Project for using Dialogflow AI

1.  Create [Google Cloud project](https://cloud.google.com/dialogflow/es/docs/quick/setup).

2.  Create [Dialogflow ES agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) with previously created GCP id.

    * Create test [Intent](https://cloud.google.com/dialogflow/es/docs/intents-overview).

    * Manually train test intent

4.  Add [service account](https://cloud.google.com/docs/authentication/getting-started). Generate json key [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#:~:text=Create%20a%20service%20account%20key%3A).

5.  Enable [Dialogflow API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) for project.

In case of code 403. IAM->PRINCIPALS->service account->add role->'Dialogflow API Admin'


## Env vars:

* VK_TOKEN=<API token VK group>
* TG_TOKEN=<[main telegram bot token](https://t.me/botfather)>
* TG_LOGS_TOKEN=<[telegram token for logs](https://t.me/botfather)>.
* TG_CHAT_ID=<bot's admin id>
* DIALOGFLOW_PROJECT_ID=<id Google Cloud Project>.
* [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable)=<kson key path>.


## Training Dialogflow agent
1. Place training data into 'learn_dialogflow\questions.json'. Format:
```
{
    <intent_name>: {
        'questions': [<question>, ...],
        'answer': <answer>
    }, ...
}
```
2. Run script with -p or -path params.
```
python learn_dialogflow.py -p questions.json
```

## Preparations for using VK group bot
1. Create group
2. ADD API key with sending messages permission.
3. Enable messages in group.


## Run


1. git clone <repository url>
2. Create virtual environment

```
python -m venv .venv
```

3. Activate venv

```
.venv\scripts\activate
```

4. Install requirements

```
pip install -r requirements.txt
```

5. Start TG bot on local machine

```
python tg_bot.py
```
