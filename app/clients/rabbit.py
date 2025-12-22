from dataclasses import dataclass

from app.config import Settings


@dataclass
class RabbitConfig:
    host: str
    port: int
    user: str
    password: str
    exchange: str


def get_rabbit_config(settings: Settings) -> RabbitConfig:
    return RabbitConfig(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        user=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
        exchange=settings.rabbitmq_exchange,
    )
