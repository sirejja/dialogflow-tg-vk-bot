# speech-bot

## Фунционал:

## Подключение Dialogflow

1.  Создать [Google Cloud project](https://cloud.google.com/dialogflow/es/docs/quick/setup).

2.  Создать [Dialogflow ES agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent) с ID ранее созданного Google Cloud проекта.

3.  Создать [Intent](https://cloud.google.com/dialogflow/es/docs/intents-overview).

4.  Добавить training phrases и Responses

5.  Добавить [service account](https://cloud.google.com/docs/authentication/getting-started). И сгенерировать json key [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#:~:text=Create%20a%20service%20account%20key%3A), который пригодится в env vars.

6.  Включить [Dialogflow API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) настраиваемого для проекта.

В случае 403 ошибки и при условии верно выполненных предыдущих шагов, может потребоваться настройка разрешений для проекта. IAM->PRINCIPALS->service account->add role->'Dialogflow API Admin'

## Обучение Dialogflow project
1. Данные для обучения поместить в 'learn_dialogflow\questions.json'. Формат обучающих данных:
```
{
    <intent_name>: {
        'questions': [<question>, ...],
        'answer': <answer>
    }, ...
}
```
2. Запустить скрипт 'learn_dialogflow\learn_dialogflow.py'

## Env vars:

Переменные окружения могут быть получены как из файла .env корневой директории, так и из ОС.

TG_TOKEN=<[токен Telegram бота](https://t.me/botfather)>

DIALOGFLOW_PROJECT_ID=<id проекта>.

[GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable)=<путь к json key файлу>.


## Запуск на windows

Git и python должны быть установлены

1. git clone <url репозитория>
2. Создание виртуального окружения

```
python -m venv .venv
```

3. Активация виртуального окружения

```
.venv\scripts\activate
```

4. Установка зависимостей

```
pip install -r requirements.txt
```

5. Запуск приложения

```
python main.py
```
