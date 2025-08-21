from typing import List, Dict

import chromadb
from sentence_transformers import SentenceTransformer

from config import settings


class EmbeddingService:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        # Инициализация модели для эмбеддингов
        self.model = SentenceTransformer(model_name)

        # Инициализация ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name="company_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[Dict[str, any]]) -> None:
        """Добавляет чанки в ChromaDB"""
        contents = [chunk['content'] for chunk in chunks]

        # Создаем эмбеддинги
        embeddings = self.model.encode(contents).tolist()

        # Подготавливаем данные для ChromaDB
        ids = [chunk['chunk_id'] for chunk in chunks]
        metadatas = [self._prepare_metadata(chunk) for chunk in chunks]

        # Добавляем в коллекцию ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )

    def search_similar(self, query: str, k: int = 5) -> List[Dict[str, any]]:
        """Ищет похожие документы"""
        # Создаем эмбеддинг запроса
        query_embedding = self.model.encode([query]).tolist()

        # Ищем в векторной базе
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k,
            include=['documents', 'metadatas', 'distances']
        )

        # Форматируем результаты
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'similarity_score': 1 - results['distances'][0][i],  # Конвертируем distance в similarity
                'chunk_id': results['ids'][0][i]
            })

        return formatted_results

    def _prepare_metadata(self, chunk: Dict[str, any]) -> Dict[str, any]:
        """Подготавливает метаданные для ChromaDB"""
        return {
            'source_url': chunk['source_url'],
            'source_title': chunk['source_title'],
            'chunk_index': chunk['chunk_index'],
            'total_chunks': chunk['total_chunks'],
            'word_count': chunk['word_count']
        }
