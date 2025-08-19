from datetime import datetime

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.core.generator import ResponseGenerator
from app.core.searcher import SearchService
from app.exceptions.exceptions import RAGException
from app.models.questions import QuestionRequest, QuestionResponse

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
@inject
async def ask_question(
        request: QuestionRequest,
        search_service: SearchService = Depends(Provide[Container.search_service]),
        response_generator: ResponseGenerator = Depends(Provide[Container.response_generator_service])
):
    """Основная апка"""

    try:
        # Поиск релевантных документов
        search_results = search_service.search_and_rank(
            query=request.question
        )

        # Генерация ответа
        answer = await response_generator.generate_response_with_sources(
            query=request.question,
            contexts=search_results
        )

        return QuestionResponse(
            answer=answer
        )

    except Exception as e:
        raise RAGException(
            detail=f"Ошибка обработки вопроса: {str(e)}",
            status_code=500,
            error_type="PROCESSING_ERROR"
        )
