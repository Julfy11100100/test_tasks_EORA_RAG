import logging
import os
from datetime import datetime

from config import settings

# Создание директории логов, если её нет
LOG_DIR = settings.LOG_FOLDER
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логгера
logger = logging.getLogger("app_logger")
logger.setLevel(settings.LOG_LEVEL)

# Формат логов
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Консольный вывод
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Вывод в файл
date_str = datetime.now().strftime("%Y-%m-%d")
log_filename = f"log_{date_str}.log"
log_file_path = os.path.join(LOG_DIR, log_filename)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setFormatter(formatter)

# Добавление хендлеров
logger.addHandler(console_handler)
logger.addHandler(file_handler)
