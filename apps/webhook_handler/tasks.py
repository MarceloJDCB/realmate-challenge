import logging
from celery import shared_task
from django.db import IntegrityError
from .services import WebhookService

logger = logging.getLogger('webhook_handler')

@shared_task
def process_webhook(data: dict) -> None:
    """
    Tarefa Celery assíncrona para processar eventos de webhook.
    
    Esta tarefa é responsável por rotear diferentes tipos de eventos
    para seus respectivos handlers no WebhookService.

    Args:
        data (dict): Dicionário contendo o tipo de evento e seus dados,
                    já validado pelo WebhookSerializer.
    """
    logger.info(f"Processing webhook event: {data['type']}")
    handlers = {
        'NEW_CONVERSATION': WebhookService.create_conversation,
        'NEW_MESSAGE': WebhookService.create_message,
        'CLOSE_CONVERSATION': WebhookService.close_conversation,
    }
    
    event_type = data['type']
    handler = handlers.get(event_type)
    
    try:
        logger.debug(f"Executing handler for {event_type} with data: {data}")
        handler(data)
        logger.info(f"Successfully processed {event_type} event")
    except Exception as e:
        logger.error(f"Error processing webhook {event_type}: {str(e)}", exc_info=True)
        raise e
