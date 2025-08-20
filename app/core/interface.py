from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, List, Dict, Any


class LLMProvider(str, Enum):
    GIGACHAT = "gigachat"
    SONAR = "sonar"


class LlmInterface(ABC):
    """Интерфейс Llm"""

    @abstractmethod
    async def generate_response(
            self,
            messages: Union[List[Dict[str, str]], list],
            **kwargs: Any
    ) -> str:
        """Абстрактный метод получения ответа от LLM"""
        pass
