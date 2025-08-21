from typing import List, Dict

import httpx

from app.core.interface import LlmInterface
from app.utils.logging import get_logger
from config import settings

logger = get_logger(__name__)


class SonarClient(LlmInterface):
    """Клиент для работы с Perplexity Sonar API"""

    def __init__(self):
        self.base_url = settings.SONAR_BASE_URL
        self.api_key = settings.SONAR_API_KEY
        self.model = settings.SONAR_MODEL

    async def generate_response(self, messages: List[Dict[str, str]],
                                temperature: float = 0.05,
                                max_tokens: int = 2000) -> str:
        """Генерация ответа через Perplexity Sonar API"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.api_key}',
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.05,  # Минимальная креативность
                "top_p": 0.8,  # Фокус на наиболее вероятных токенах
                "max_tokens": 2000,  # Больше места для детального анализа

                "search_domain_filter": ['eora.ru'],
                "return_images": False,
                "return_related_questions": False,
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                result = response.json()
                logger.info(f"SONAR RESULT: {result}")

                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
                else:
                    raise Exception("Некорректный ответ от Sonar API")

        except Exception as e:
            logger.error(f"Ошибка генерации ответа Sonar: {e}")
            raise Exception(f"Ошибка обращения к Sonar: {e}")
