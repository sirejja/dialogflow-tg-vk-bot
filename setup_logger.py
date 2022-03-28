import logging
import os
from telegram import Bot
from dotenv import load_dotenv


_log_format = (
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s)"
    ".%(funcName)s(%(lineno)d) - %(message)s"
)


class LogBotHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )


def setup_logger():
    load_dotenv()

    logger = logging.getLogger()

    bot_handler = LogBotHandler(
        Bot(token=os.environ['TG_LOGS_TOKEN']),
        os.environ['TG_CHAT_ID']
    )
    bot_handler.setLevel(logging.DEBUG)
    bot_handler.setFormatter(logging.Formatter(_log_format))

    logger.addHandler(bot_handler)

    return logger
