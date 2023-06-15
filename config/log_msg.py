# main
LOG_START = 'Logging START'
BOT_START = 'Bot START'
MAIN_ERR_MSG = 'Сбой в работе программы = {}'
MAIN_STATUS = 'Статус работы не изменился'
MAIN_STOP = 'Bot STOPPED'

# check_tokens
TOKEN_WRONG = 'Отсутствует переменная окружения {}. Работа будет остановлена'
TOKEN_OK = 'Проверка переменных окружения ОК'

# get_api_answer
API_REQUESTS = 'Запрос отправлен'
API_RESPONSE = 'Ответ получен'
CODE_WRONG = 'Код ответа API = {}, {}'

# check_response
CHECK_RESPONSE = 'Проверка данных в ответе сервера START'
RESPONSE_OK = 'Проверка данных в ответе сервера OK'
ERR_DATA_TYPE = 'Тип данных в ответе {}, не соответствует ожидаемому {}'
DATA_NONE = 'Данные в ответе сервера отсутствуют. {} is None'

# parse_status
PARS_START = 'Парсинг данных START'
PARS_OK = 'Парсинг данных OK'
STATUS_WRONG = 'Неизвестный статус работы'
HOMEWORK_NONE = 'Отсутствует ключ {}'
STATUS_CHANGE = 'Изменился статус проверки работы "{}" {}'

# send_message
TRY_MSG = 'Отправка сообщения START'
MSG_OK = 'Отправка сообщения OK'
MSG_FAIL = 'Отправка сообщения FAIL'

# setup_logging
LOG_CONFIG_OK = 'Конфигурация logging успешно загружена'
LOG_CONFIG_WRONG = (
    'Конфигурация logging не найдена, будет использована базовая'
)

# write_timestamp
WRITE_OK = 'Запись временной метки в файл OK'

# read_timestamp
READ_OK = 'Чтение временной метки из файла OK'
