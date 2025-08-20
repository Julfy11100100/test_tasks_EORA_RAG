from typing import List, Dict

from app.constants.generator import ANSWER_PROMPT, SYSTEM_PROMPT, NO_ANSWER_STR
from app.core.gigachat import GigaChatClient
from app.utils.logging import logger
from config import settings


class ResponseGenerator:
    def __init__(self):
        self.gigachat_client = GigaChatClient()

    async def generate_response_with_sources(self, query: str,
                                             contexts: List[Dict]) -> str:
        """Генерирует ответ с указанием источников"""
        if not contexts:
            return NO_ANSWER_STR

        # Подготавливаем контекст для GigaChat
        context_text = self._prepare_context(contexts)

        # Создаем сообщения для чата
        messages = [
            {
                "role": "system",
                "content": self._get_system_prompt()
            },
            {
                "role": "user",
                "content": self._create_prompt(query, context_text)
            }
        ]

        try:
            # Отправляем запрос к GigaChat
            answer = await self.gigachat_client.generate_response(
                messages=messages,
                temperature=settings.TEMPERATURE,
                max_tokens=500
            )

            logger.info(f"Отправилит запрос к GigaChat: {messages}\n"
                        f"Получили ответ:\n"
                        f"{answer}")

            return answer

        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return "Извините, произошла ошибка при формировании ответа."

    def _get_system_prompt(self) -> str:
        """Системный промт для настройки поведения GigaChat"""
        return SYSTEM_PROMPT

    def _create_prompt(self, query: str, context: str) -> str:
        """Создает промт для генерации ответа"""
        return f"""
        {context}

        Вопрос клиента: {query}

        {ANSWER_PROMPT}
        """

    def _prepare_context(self, contexts: List[Dict]) -> str:
        """Подготавливает контекст для GigaChat"""
        context_parts = []

        for i, ctx in enumerate(
                contexts[:settings.MAX_SEARCH_RESULTS]):  # Используем топ-MAX_SEARCH_RESULTS результатов
            source_info = f"Источник: {ctx['metadata']['source_title']}"
            content = f"Контекст: {ctx['content']}"
            url = f"Ссылка: {ctx['metadata']['source_url']}"
            context_parts.append(f"{source_info}\n{content}\n{url}\n")

        return "\n---\n".join(context_parts)
