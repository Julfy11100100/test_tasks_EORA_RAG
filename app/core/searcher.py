from typing import List, Dict

from app.core.embedding import EmbeddingService
from config import settings


class SearchService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.min_similarity_threshold = settings.MIN_SIMILARITY_THRESHOLD

    def search_and_rank(self, query: str, k: int = 5) -> List[Dict[str, any]]:
        """Ищет и ранжирует релевантные документы"""
        # Получаем первичные результаты, берём в два раза больше чтобы потом отсечь
        raw_results = self.embedding_service.search_similar(query, k * 2)

        # Фильтруем по порогу релевантности
        filtered_results = [
            result for result in raw_results
            if result['similarity_score'] > self.min_similarity_threshold
        ]

        if not filtered_results:
            return []

        # Применяем дополнительную логику ранжирования
        ranked_results = self._apply_ranking_logic(filtered_results, query)

        # Возвращаем топ-k результатов
        return ranked_results[:k]

    def _apply_ranking_logic(self, results: List[Dict], query: str) -> List[Dict]:
        """Применяет дополнительную логику ранжирования"""
        for result in results:
            base_score = result['similarity_score']

            # Бонус за длину контента (более информативные чанки)
            # Если чанк длинный, возможно он более информативный
            content_length_bonus = min(0.1, len(result['content'].split()) / 1000)

            # Бонус за наличие ключевых слов в заголовке
            # Если ключевые слова есть в заголовке, скорее всего текст информативный
            title_bonus = self._calculate_title_bonus(
                result['metadata']['source_title'],
                query
            )

            # Итоговый скор
            result['final_score'] = base_score + content_length_bonus + title_bonus

        # Сортируем по итоговому скору
        return sorted(results, key=lambda x: x['final_score'], reverse=True)

    def _calculate_title_bonus(self, title: str, query: str) -> float:
        """Вычисляет бонус за совпадения в заголовке"""
        title_words = set(title.lower().split())
        query_words = set(query.lower().split())

        intersection = title_words.intersection(query_words)
        if intersection:
            return 0.2 * (len(intersection) / len(query_words))

        return 0.0

    def has_relevant_information(self, results: List[Dict]) -> bool:
        """Проверяет, есть ли релевантная информация"""
        return bool(results) and results[0]['similarity_score'] > 0.4
