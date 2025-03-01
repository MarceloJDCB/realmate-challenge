import pytest
import uuid
from apps.webhook_handler.models import Conversation, Message
from apps.webhook_handler.services import WebhookService
from apps.webhook_handler.factories import ConversationFactory


@pytest.mark.django_db
class TestWebhookService:
    def test_create_conversation(self):
        conversation_id = str(uuid.uuid4())
        data = {
            'type': 'NEW_CONVERSATION',
            'timestamp': '2025-02-21T10:20:41.349308',
            'data': {'id': conversation_id}
        }

        conversation = WebhookService.create_conversation(data)
        assert conversation.id == conversation_id
        assert conversation.state == Conversation.OPEN_CHOICE

    def test_create_message(self):
        conversation = ConversationFactory()
        message_id = str(uuid.uuid4())
        data = {
            'type': 'NEW_MESSAGE',
            'timestamp': '2025-02-21T10:20:42.349308',
            'data': {
                'id': message_id,
                'direction': 'RECEIVED',
                'content': 'Test message',
                'conversation_id': str(conversation.id)
            }
        }

        message = WebhookService.create_message(data)
        assert message.id == message_id
        assert message.conversation == conversation
        assert message.direction == Message.RECEIVED_CHOICE
        assert message.content == 'Test message'

    def test_create_message_closed_conversation(self):
        conversation = ConversationFactory(state=Conversation.CLOSED_CHOICE)
        data = {
            'type': 'NEW_MESSAGE',
            'timestamp': '2025-02-21T10:20:42.349308',
            'data': {
                'id': str(uuid.uuid4()),
                'direction': 'RECEIVED',
                'content': 'Test message',
                'conversation_id': str(conversation.id)
            }
        }

        with pytest.raises(ValueError):
            WebhookService.create_message(data)

    def test_close_conversation(self):
        conversation = ConversationFactory()
        data = {
            'type': 'CLOSE_CONVERSATION',
            'timestamp': '2025-02-21T10:20:45.349308',
            'data': {'id': str(conversation.id)}
        }

        updated_conversation = WebhookService.close_conversation(data)
        assert updated_conversation.state == Conversation.CLOSED_CHOICE
