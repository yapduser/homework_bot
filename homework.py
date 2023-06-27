import logging
import os
import re
import time

import requests
import telegram
from dotenv import load_dotenv

import config.log_msg as msg
from config.logging_config import setup_logging
from time_keeper.processor import read_timestamp, write_timestamp

load_dotenv()

logger = logging.getLogger(__name__)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('ACCOUNT_SID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HW = 'homeworks'
DATE = 'current_date'
STATUS = 'status'
HW_NAME = 'homework_name'
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.',
}


def check_tokens():
    """Проверка переменных окружения."""
    env_vars = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    for key, value in env_vars.items():
        if not value:
            logger.critical(msg.TOKEN_WRONG.format(key))
            raise SystemExit

    logger.debug(msg.TOKEN_OK)


def get_api_answer(timestamp):
    """Запрос к API."""
    logger.debug(msg.API_REQUESTS)
    payload = {'from_date': timestamp}
    try:
        response = requests.get(
            url=ENDPOINT, headers=HEADERS, params=payload, timeout=5
        )
    except requests.RequestException as error:
        error = re.sub(re.compile(r'at 0x[0-9a-fA-F]+'), '', str(error))
        raise Exception(error)

    if response.status_code != requests.codes.ok:
        raise requests.HTTPError(
            msg.CODE_WRONG.format(response.status_code, response.text)
        )

    logger.debug(msg.API_RESPONSE)
    return response.json()


def check_response(response):
    """Проверка ответа API."""
    logger.debug(msg.CHECK_RESPONSE)
    if not isinstance(response, dict):
        raise TypeError(msg.ERR_DATA_TYPE.format(type(response), dict))

    for key in (HW, DATE):
        if response.get(key) is None:
            raise KeyError(msg.DATA_NONE.format(key))

    if not isinstance(response[HW], list):
        raise TypeError(msg.ERR_DATA_TYPE.format(type(response[HW]), list))

    logger.debug(msg.RESPONSE_OK)


def parse_status(homework):
    """Получает данные из ответа API."""
    logger.debug(msg.PARS_START)
    status = homework.get(STATUS)
    if status not in HOMEWORK_VERDICTS:
        raise KeyError(msg.STATUS_WRONG)

    if HW_NAME not in homework:
        raise KeyError(msg.HOMEWORK_NONE.format(HW_NAME))

    homework_name = re.sub(r'^.*?__|\.zip$', '', homework[HW_NAME])
    verdict = HOMEWORK_VERDICTS[status]
    logger.debug(msg.PARS_OK)
    message = msg.STATUS_CHANGE.format(homework_name, verdict)
    logger.info(message)
    return message


def send_message(bot, message):
    """Отправляет сообщение в чат."""
    try:
        logger.debug(msg.TRY_MSG)
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(msg.MSG_OK)
        return True
    except telegram.error.TelegramError:
        logger.exception(msg.MSG_FAIL)


def main():
    """Основная логика работы бота."""
    check_tokens()
    logger.info(msg.BOT_START)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = read_timestamp()
    message = f'{msg.BOT_START}. \n{msg.MAIN_STATUS}'
    last_message = None

    while True:
        logger.debug('****************************************')
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            timestamp = response.get(DATE, timestamp)
            write_timestamp(timestamp)
            homework = response[HW]
            if homework:
                message = parse_status(homework[0])
        except Exception as error:
            message = msg.MAIN_ERR_MSG.format(error)
            logger.exception(message)

        if message != last_message and send_message(bot, message):
            last_message = message
        else:
            logger.debug(msg.MAIN_STATUS)

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    setup_logging()
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error(msg.MAIN_STOP)
