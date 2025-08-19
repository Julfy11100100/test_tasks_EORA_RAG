import pytest

from app.core.chunker import ContentChunker


@pytest.fixture
def chunker():
    return ContentChunker(chunk_size=10, overlap=2)


def test_short_document(chunker):
    document = {
        'url': 'https://example.com',
        'title': 'Тест',
        'content': 'Один два три четыре пять шесть семь восемь'
    }

    chunks = chunker.chunk_document(document)
    assert len(chunks) == 1
    assert chunks[0]['chunk_index'] == 0
    assert chunks[0]['total_chunks'] == 1
    assert chunks[0]['word_count'] == 8


def test_empty_document(chunker):
    document = {
        'url': 'https://example.com',
        'title': 'Тест',
        'content': ''
    }

    chunks = chunker.chunk_document(document)
    assert len(chunks) == 1
    assert chunks[0]['word_count'] == 0
    assert chunks[0]['content'] == ''
