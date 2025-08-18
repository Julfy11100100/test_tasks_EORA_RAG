import logging
import os

from config import settings

# Создание директории логов, если её нет
LOG_DIR = settings.LOG_FOLDER
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логгера
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Консольный вывод
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавление хендлеров
logger.addHandler(console_handler)
