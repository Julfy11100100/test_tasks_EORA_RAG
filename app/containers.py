from dependency_injector import containers, providers

from app.core.embedding import EmbeddingService
from app.core.generator import ResponseGenerator
from app.core.searcher import SearchService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    embedding_service = providers.Factory(
        EmbeddingService
    )

    response_generator_service = providers.Factory(
        ResponseGenerator
    )

    search_service = providers.Factory(
        SearchService,
        embedding_service=embedding_service
    )
