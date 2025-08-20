from typing import Dict, Type

from app.core.sonar import SonarClient
from app.core.gigachat import GigaChatClient
from app.core.interface import LLMProvider
from app.core.interface import LlmInterface


class LLMClientFactory:
    """Фабрика для создания LLM клиентов"""

    _clients: Dict[LLMProvider, Type[LlmInterface]] = {
        LLMProvider.GIGACHAT: GigaChatClient,
        LLMProvider.SONAR: SonarClient,
    }

    @classmethod
    def create_client(cls, provider: LLMProvider, **kwargs) -> LlmInterface:
        """Создает клиент для указанного провайдера"""
        if provider not in cls._clients:
            raise ValueError(f"Неподдерживаемый провайдер: {provider}")

        client_class = cls._clients[provider]
        return client_class(**kwargs)
