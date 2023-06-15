import os
import json
import logging

import config.log_msg as msg

logger = logging.getLogger(__name__)

PATH = 'time_keeper/timestamp.json'


def write_timestamp(timestamp=0):
    """Записать timestamp в файл."""
    data = {'timestamp': timestamp}
    with open(PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file)
    logger.debug(msg.WRITE_OK)


def read_timestamp():
    """Прочитать файл и вернуть timestamp."""
    if not os.path.exists(PATH):
        write_timestamp()

    with open(PATH, 'r', encoding='utf-8') as file:
        timestamp = json.load(file)
    logger.debug(msg.READ_OK)
    return timestamp['timestamp']
