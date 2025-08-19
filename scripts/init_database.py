#!/usr/bin/env python3
"""Скрипт для первичной инициализации базы данных"""

import asyncio
import sys
from pathlib import Path

from app.core.chunker import ContentChunker
from app.core.embedding import EmbeddingService
from app.core.parser import HTMLParser
from app.utils.logging import logger
from config import settings

sys.path.append(str(Path(__file__).parent.parent))


async def init_knowledge_base():
    """Инициализация базы знаний"""
    logger.info("Начинаем инициализацию базы знаний.")

    # URLs
    company_urls = [
        "https://eora.ru/cases/promyshlennaya-bezopasnost",
        "https://eora.ru/cases/lamoda-systema-segmentacii-i-poiska-po-pohozhey-odezhde",
        "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/karas-golosovoy-assistent",
        "https://eora.ru/cases/assistenty-dlya-gorodov",
        "https://eora.ru/cases/avtomatizaciya-v-promyshlennosti/chemrar-raspoznovanie-molekul",
        "https://eora.ru/cases/zeptolab-skazki-pro-amnyama-dlya-sberbox",
        "https://eora.ru/cases/goosegaming-algoritm-dlya-ocenki-igrokov",
        "https://eora.ru/cases/dodo-pizza-robot-analitik-otzyvov",
        "https://eora.ru/cases/ifarm-nejroset-dlya-ferm",
        "https://eora.ru/cases/zhivibezstraha-navyk-dlya-proverki-rodinok",
        "https://eora.ru/cases/sportrecs-nejroset-operator-sportivnyh-translyacij",
        "https://eora.ru/cases/avon-chat-bot-dlya-zhenshchin",
        "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/navyk-dlya-proverki-loterejnyh-biletov",
        "https://eora.ru/cases/computer-vision/iss-analiz-foto-avtomobilej",
        "https://eora.ru/cases/purina-master-bot",
        "https://eora.ru/cases/skinclub-algoritm-dlya-ocenki-veroyatnostej",
        "https://eora.ru/cases/skolkovo-chat-bot-dlya-startapov-i-investorov",
        "https://eora.ru/cases/purina-podbor-korma-dlya-sobaki",
        "https://eora.ru/cases/purina-navyk-viktorina",
        "https://eora.ru/cases/dodo-pizza-pilot-po-avtomatizacii-kontakt-centra",
        "https://eora.ru/cases/dodo-pizza-avtomatizaciya-kontakt-centra",
        "https://eora.ru/cases/icl-bot-sufler-dlya-kontakt-centra",
        "https://eora.ru/cases/s7-navyk-dlya-podbora-aviabiletov",
        "https://eora.ru/cases/workeat-whatsapp-bot",
        "https://eora.ru/cases/absolyut-strahovanie-navyk-dlya-raschyota-strahovki",
        "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
        "https://eora.ru/cases/kazanexpress-sistema-rekomendacij-na-sajte",
        "https://eora.ru/cases/intels-proverka-logotipa-na-plagiat",
        "https://eora.ru/cases/karcher-viktorina-s-voprosami-pro-uborku",
        "https://eora.ru/cases/chat-boty/purina-friskies-chat-bot-na-sajte",
        "https://eora.ru/cases/nejroset-segmentaciya-video",
        "https://eora.ru/cases/chat-boty/essa-nejroset-dlya-generacii-rolikov",
        "https://eora.ru/cases/qiwi-poisk-anomalij",
        "https://eora.ru/cases/frisbi-nejroset-dlya-raspoznavaniya-pokazanij-schetchikov",
        "https://eora.ru/cases/skazki-dlya-gugl-assistenta",
        "https://eora.ru/cases/chat-boty/hr-bot-dlya-magnit-kotoriy-priglashaet-na-sobesedovanie"
    ]

    try:
        # Инициализация сервисов
        parser = HTMLParser()
        chunker = ContentChunker(
            chunk_size=settings.DEFAULT_CHUNK_SIZE,
            overlap=settings.DEFAULT_CHUNK_OVERLAP
        )
        embedding_service = EmbeddingService()

        logger.info(f"Обработка {len(company_urls)} страниц.")

        all_chunks = []

        for i, url in enumerate(company_urls, 1):
            logger.info(f"[{i}/{len(company_urls)}] Обработка: {url}")

            # Парсинг страницы
            document = parser.parse_page(url)
            if document:
                # Чанкинг
                chunks = chunker.chunk_document(document)
                all_chunks.extend(chunks)
                logger.info(f"Создано {len(chunks)} чанков")
            else:
                logger.info(f"Ошибка парсинга")

        # Добавление в векторную БД
        logger.info(f"Добавление {len(all_chunks)} чанков в векторную БД.")
        embedding_service.add_documents(all_chunks)

        logger.info("Инициализация завершена успешно!")
        logger.info(f"Обработано страниц: {len([url for url in company_urls])}")
        logger.info(f"Создано чанков: {len(all_chunks)}")

    except Exception as e:
        logger.error(f"Ошибка инициализации: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_knowledge_base())
