import re
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

from app.utils.logging import get_logger

logger = get_logger(__name__)


class HTMLParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
        })

    def parse_page(self, url: str) -> Optional[Dict[str, str]]:
        """Извлекает структурированную информацию со страницы"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            unwanted_tags = [
                'script', 'style', 'nav', 'footer', 'header',
                '.sidebar', '.menu', '.ads', '.popup', '.modal',
                '.cookie-banner', '.newsletter', '.comments'
            ]

            for selector in unwanted_tags:
                for tag in soup.select(selector):
                    tag.decompose()

            # Извлекаем основную информацию
            title = self._extract_title(soup)
            content = self._extract_content(soup)

            if not content.strip():
                logger.warning(f"Пустой контент для {url}")
                return None

            return {
                'url': url,
                'title': title,
                'content': self._clean_text(content),
                'word_count': len(content.split()),
                'char_count': len(content)
            }

        except requests.RequestException as e:
            logger.error(f"Ошибка запроса {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлекает заголовок страницы"""
        title_selectors = [
            'h1',
            '.case-title',
            '.project-title',
            '.page-title',
            '.entry-title',
            '.post-title',
            'title'
        ]

        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()

        return "Без названия"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Извлекает основной контент"""
        # Приоритетные селекторы для контента
        content_selectors = [
            'main',
            'article',
            '.case-content',
            '.project-details',
            '.content',
            '.post-content',
            '.article-content',
            '.entry-content',
            '#content',
            '.project-description',
            '.main-content'
        ]

        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text()
                if len(text.strip()) > 100:  # Минимальная длина контента
                    return text

        # Если специфичные селекторы не найдены, пробуем body
        # но исключаем навигацию и служебные элементы
        body = soup.find('body')
        if body:
            # Удаляем из body служебные элементы
            for unwanted in body.select('.navigation, .menu, .sidebar, .footer, .header'):
                unwanted.decompose()
            return body.get_text()

        return ""

    def _clean_text(self, text: str) -> str:
        """Очищает текст от лишних символов"""
        # Удаляем множественные пробелы и переносы
        text = re.sub(r'\s+', ' ', text)
        # Удаляем специальные символы
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]"\'«»]', '', text)
        # Убираем специфичный для сайта Eora текст
        text = self._specific_clean_text(text)

        return text.strip()

    def _specific_clean_text(self, text: str) -> str:
        """Убираем специфичный для сайта Eora текст"""

        # Удаление любых массивов, начинающихся с '[' и заканчивающихся на ']'
        text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)

        # Удаляем специфичные фразы
        to_remove = [
            "Нажимая на кнопку, вы соглашаетесь с нашей Политикой в отношении обработки персональных данных пользователей",
            "Перейти в портфолио Обязательное поле",
            "Пожалуйста, введите корректный e-mail адрес",
            "Пожалуйста, введите корректное имя",
            "Пожалуйста, введите корректный номер телефона",
            "Слишком короткое значение Send Обязательное поле"
        ]

        for phrase in to_remove:
            text = re.sub(phrase, '', text, flags=re.IGNORECASE | re.DOTALL)

        return text
