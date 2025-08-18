import re
from typing import Dict

import requests
from bs4 import BeautifulSoup
from app.utils.logging import logger


class HTMLParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; RAG-bot/1.0)'
        })

    def parse_page(self, url: str) -> Dict[str, str]:
        """Извлекает структурированную информацию со страницы"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Удаляем ненужные элементы
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()

            # Извлекаем основную информацию
            title = self._extract_title(soup)
            content = self._extract_content(soup)

            return {
                'url': url,
                'title': title,
                'content': self._clean_text(content),
                'word_count': len(content.split())
            }

        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлекает заголовок страницы"""
        title_selectors = ['h1', 'title', '.page-title', '.project-title']

        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()

        return "Без названия"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Извлекает основной контент"""
        # Приоритетные селекторы для контента
        content_selectors = [
            'main', '.content', '.post-content',
            '.article-content', '#content', '.project-description'
        ]

        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text()

        # Если специфичные селекторы не найдены, берем весь body
        body = soup.find('body')
        return body.get_text() if body else ""

    def _clean_text(self, text: str) -> str:
        """Очищает текст от лишних символов"""
        # Удаляем множественные пробелы и переносы
        text = re.sub(r'\s+', ' ', text)
        # Удаляем специальные символы
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]"\'«»]', '', text)
        return text.strip()
