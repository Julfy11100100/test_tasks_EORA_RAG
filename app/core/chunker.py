import math
from typing import List, Dict


class ContentChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document: Dict[str, str]) -> List[Dict[str, any]]:
        """Разбивает документ на чанки"""
        content = document['content']
        words = content.split()

        if len(words) <= self.chunk_size:
            return [self._create_chunk(document, content, 0, 1)]

        chunks = []
        total_chunks = math.ceil(len(words) / (self.chunk_size - self.overlap))

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_content = ' '.join(chunk_words)

            chunk = self._create_chunk(
                document,
                chunk_content,
                len(chunks),
                total_chunks
            )
            chunks.append(chunk)

            if i + self.chunk_size >= len(words):
                break

        return chunks

    def _create_chunk(self, document: Dict, content: str,
                      index: int, total: int) -> Dict[str, any]:
        """Создает чанк с метаданными"""
        return {
            'chunk_id': f"{document['url']}#chunk_{index}",
            'content': content,
            'source_url': document['url'],
            'source_title': document['title'],
            'chunk_index': index,
            'total_chunks': total,
            'word_count': len(content.split())
        }
