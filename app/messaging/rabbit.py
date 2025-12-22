import json
import logging
from typing import Any, Dict

import pika

from app.clients.rabbit import RabbitConfig, get_rabbit_config
from app.config import get_settings

logger = logging.getLogger(__name__)


class RabbitPublisher:
    def __init__(self, config: RabbitConfig):
        credentials = pika.PlainCredentials(config.user, config.password)
        self.params = pika.ConnectionParameters(host=config.host, port=config.port, credentials=credentials)
        self.exchange = config.exchange

    def publish(self, routing_key: str, payload: Dict[str, Any]) -> None:
        try:
            connection = pika.BlockingConnection(self.params)
            channel = connection.channel()
            channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
            body = json.dumps(payload).encode("utf-8")
            channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=body)
            connection.close()
        except Exception as exc:
            logger.warning("Failed to publish event %s: %s", routing_key, exc)


_publisher: RabbitPublisher | None = None


def get_publisher() -> RabbitPublisher:
    global _publisher
    if _publisher is None:
        settings = get_settings()
        cfg = get_rabbit_config(settings)
        _publisher = RabbitPublisher(cfg)
    return _publisher
