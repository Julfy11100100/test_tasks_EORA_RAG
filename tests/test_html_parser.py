from unittest.mock import patch, MagicMock

import pytest
from bs4 import BeautifulSoup

from app.core.parser import HTMLParser


@pytest.fixture
def parser():
    return HTMLParser()


def test_clean_text(parser):
    raw_text = " Это тестовый@#@@    текст, для проверки №№№на удаление   экстрасимволов..."
    cleaned_text = parser._clean_text(raw_text)
    assert cleaned_text == "Это тестовый текст, для проверки на удаление экстрасимволов..."


def test_extract_title_from_h1(parser):
    html = "<html><body><h1>Заголовок</h1></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    title = parser._extract_title(soup)
    assert title == "Заголовок"


def test_extract_title_fallback(parser):
    html = "<html><body><div>Нет заголовка</div></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    title = parser._extract_title(soup)
    assert title == "Без названия"


def test_extract_content_from_main(parser):
    html = "<html><body><main>Основной контент</main></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    content = parser._extract_content(soup)
    assert "Основной контент" in content


def test_extract_content_fallback_to_body(parser):
    html = "<html><body>Контент в body</body></html>"
    soup = BeautifulSoup(html, "html.parser")
    content = parser._extract_content(soup)
    assert "Контент в body" in content


@patch("app.core.parser.requests.Session.get")
def test_parse_page_success(mock_get, parser):
    html = """
    <html>
        <head><title>Тестовая страница</title></head>
        <body><main>Контент страницы</main></body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.content = html.encode("utf-8")
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    result = parser.parse_page("http://example.com")
    assert result["title"] == "Тестовая страница"
    assert "Контент страницы" in result["content"]
    assert result["url"] == "http://example.com"
    assert result["word_count"] > 0
