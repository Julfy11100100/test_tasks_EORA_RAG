from typing import List, Dict, Tuple

from app.constants.generator import SYSTEM_PROMPT, NO_ANSWER_STR, ANSWER_PROMPT
from app.core.interface import LLMProvider
from app.core.llm_factory import LLMClientFactory
from app.utils.logging import get_logger
from config import settings

logger = get_logger(__name__)


class ResponseGenerator:
    def __init__(self):
        provider = LLMProvider(settings.LLM_PROVIDER)
        self.llm_client = LLMClientFactory.create_client(provider)

    async def generate_response_with_sources(self, query: str,
                                             contexts: List[Dict]) -> str:
        """Генерирует ответ с указанием источников"""
        if not contexts:
            return NO_ANSWER_STR

        # Подготавливаем контекст
        context_text, links = self._prepare_context_and_links(contexts)

        # Создаем сообщения для чата
        messages = [
            {
                "role": "system",
                "content": self._get_system_prompt()
            },
            {
                "role": "user",
                "content": self._create_prompt(query, context_text, links)
            }
        ]

        try:
            # Отправляем запрос
            answer = await self.llm_client.generate_response(
                messages=messages,
                temperature=settings.TEMPERATURE,
                max_tokens=500
            )

            logger.info(f"Отправилит запрос: {messages}\n"
                        f"Получили ответ:\n"
                        f"{answer}")

            return answer

        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return "Извините, произошла ошибка при формировании ответа."

    def _get_system_prompt(self) -> str:
        """Системный промт для настройки поведения"""
        return SYSTEM_PROMPT

    def _create_prompt(self, query: str, context: str, links: str) -> str:
        """Создает промт для генерации ответа"""

        return f"""
        Контекст:
        {context}

        Ссылки:
        {links}

        Вопрос клиента:
        {query}

        {ANSWER_PROMPT}
        """

    def _prepare_context_and_links(self, contexts: List[Dict]) -> Tuple[str, str]:
        """Подготавливает контекст и ссылки для промта"""
        context_parts = []
        links = []

        for i, ctx in enumerate(contexts[:settings.MAX_SEARCH_RESULTS]):
            source_info = f"Источник: {ctx['metadata']['source_title']}"
            content = f"Контекст: {ctx['content']}"
            url = f"Ссылка: {ctx['metadata']['source_url']}"
            context_parts.append(f"{source_info} {content} {url}\n")
            links.append(ctx['metadata']['source_url'])

        return "\n---\n".join(context_parts), "\n---\n".join(links)
