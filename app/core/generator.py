from typing import List, Dict

from app.constants.generator import ANSWER_PROMT, SYSTEM_PROMT, NO_ANSWER_STR
from app.core.gigachat import GigaChatClient
from app.utils.logging import logger


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
                temperature=0.7,
                max_tokens=500
            )

            logger.info(f"Отправилит запрос к GigaChat: {messages}"
                        f"Получили ответ: {answer}")

            return answer

        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return "Извините, произошла ошибка при формировании ответа."

    def _get_system_prompt(self) -> str:
        """Системный промт для настройки поведения GigaChat"""
        return SYSTEM_PROMT

    def _create_prompt(self, query: str, context: str) -> str:
        """Создает промт для генерации ответа"""
        return f"""
        Контекст о компании:
        {context}

        Вопрос клиента: {query}

        {ANSWER_PROMT}
        """

    def _prepare_context(self, contexts: List[Dict]) -> str:
        """Подготавливает контекст для GigaChat"""
        context_parts = []

        for i, ctx in enumerate(contexts[:5]):  # Используем топ-5 результатов
            source_info = f"Источник: {ctx['metadata']['source_title']}"
            content = ctx['content']
            url = ctx['metadata']['source_url']
            context_parts.append(f"{source_info}\n{content}\n{url}\n")

        return "\n---\n".join(context_parts)
