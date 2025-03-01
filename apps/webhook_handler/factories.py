import uuid
from datetime import datetime
import factory
from factory.django import DjangoModelFactory
from .models import Conversation, Message


class ConversationFactory(DjangoModelFactory):
    class Meta:
        model = Conversation

    id = factory.LazyFunction(uuid.uuid4)
    state = Conversation.OPEN_CHOICE


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    id = factory.LazyFunction(uuid.uuid4)
    conversation = factory.SubFactory(ConversationFactory)
    direction = Message.RECEIVED_CHOICE
    content = factory.Faker('text', max_nb_chars=200)
    timestamp = factory.LazyFunction(datetime.now)
