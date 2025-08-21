import logging
import os
from datetime import datetime

from config import settings


def setup_logger(name: str = None) -> logging.Logger:
    if name is None:
        import inspect
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame)  # Добавляем  здесь!
        if module and hasattr(module, '__name__'):
            name = module.__name__
        else:
            name = 'default_logger'

    # Проверяем, не настроен ли уже этот логгер
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Логгер уже настроен

    # Создание директории логов
    LOG_DIR = settings.LOG_FOLDER
    os.makedirs(LOG_DIR, exist_ok=True)

    logger.setLevel(settings.LOG_LEVEL)

    # Формат логов
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Вывод в файл
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"log_{date_str}.log"
    log_file_path = os.path.join(LOG_DIR, log_filename)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Предотвращаем дублирование логов в родительских логгерах
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """Получает логгер с именем вызывающего модуля"""
    return setup_logger(name)
