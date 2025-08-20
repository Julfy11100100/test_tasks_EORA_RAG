import time
import uuid

import httpx

from app.core.interface import LlmInterface
from app.utils.logging import get_logger
from config import settings

logger = get_logger(__name__)

class GigaChatClient(LlmInterface):
    """Клиент для работы с GigaChat API"""

    def __init__(self):
        self.base_url = settings.GIGACHAT_BASE_URL
        self.api_key = settings.GIGACHAT_API_KEY
        self.scope = settings.GIGACHAT_SCOPE
        self.model = settings.GIGACHAT_MODEL
        self.access_token = None
        self.token_expires_at = 0

    async def _get_access_token(self) -> str:
        """Получение access token для GigaChat"""
        if self.access_token and time.time() < self.token_expires_at - 300:  # 5 минут запас
            return self.access_token

        auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Basic {self.api_key}'
        }

        data = {
            'scope': self.scope
        }

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(auth_url, headers=headers, data=data)
                response.raise_for_status()

                token_data = response.json()
                self.access_token = token_data['access_token']
                # Время жизни токена обычно 30 минут
                self.token_expires_at = time.time() + token_data.get('expires_in', 1800)

                logger.info("GigaChat access_token получен успешно")
                return self.access_token

            except Exception as e:
                logger.error(f"Ошибка получения токена GigaChat: {e}")
                raise Exception(f"Не удалось получить токен доступа: {e}")

    async def generate_response(self, messages: list, temperature: float = 0.7,
                                max_tokens: int = 512) -> str:
        """Генерация ответа через GigaChat API"""
        try:
            access_token = await self._get_access_token()

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'X-Request-ID': str(uuid.uuid4())
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "repetition_penalty": 1.1,
                "update_interval": 0
            }

            async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                result = response.json()

                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
                else:
                    raise Exception("Некорректный ответ от GigaChat API")

        except Exception as e:
            logger.error(f"Ошибка генерации ответа GigaChat: {e}")
            raise Exception(f"Ошибка обращения к GigaChat: {e}")
