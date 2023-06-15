import logging.config

import yaml

import config.log_msg as msg


PATH = 'config/logging.yaml'


def setup_logging():
    """Настройка формата логов."""
    logger = logging.getLogger()
    try:
        with open(PATH, 'r', encoding='utf-8') as file:
            loging_config = yaml.safe_load(file)
        logging.config.dictConfig(loging_config)
        logger.debug(msg.LOG_CONFIG_OK)
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning(msg.LOG_CONFIG_WRONG)

    logger.info(msg.LOG_START)
