from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class QuestionRequest(BaseModel):
    question: str = Field("Что вы можете сделать для ритейлеров?", min_length=10, max_length=500,
                          description="Вопрос клиента")

    @field_validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Вопрос не может быть пустым')
        return v.strip()


class QuestionResponse(BaseModel):
    answer: str
