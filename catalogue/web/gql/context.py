from aiokafka import AIOKafkaProducer
from fastapi import Depends
from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from catalogue.db.dependencies import get_db_session
from catalogue.services.kafka.dependencies import get_kafka_producer
from catalogue.services.redis.dependency import get_redis_pool


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        redis_pool: ConnectionPool = Depends(get_redis_pool),
        db_connection: AsyncSession = Depends(get_db_session),
        kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
    ) -> None:
        self.redis_pool = redis_pool
        self.db_connection = db_connection
        self.kafka_producer = kafka_producer
        pass  # noqa: WPS420


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
