from celery.shared_task import shared_task
from .services import WebhookService


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
    handlers = {
        'NEW_CONVERSATION': WebhookService.create_conversation,
        'NEW_MESSAGE': WebhookService.create_message,
        'CLOSE_CONVERSATION': WebhookService.close_conversation,
    }
    event_type = data['type']
    handler = handlers.get(event_type)
    handler(data)
