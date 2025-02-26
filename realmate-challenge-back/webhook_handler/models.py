from django.db import models

class Conversation(models.Model):
    """
    Modelo que representa uma conversa no sistema.
    
    Attributes:
        id (UUIDField): Identificador único da conversa
        state (CharField): Estado atual da conversa (OPEN ou CLOSED)
        created_at (DateTimeField): Data e hora de criação da conversa
        updated_at (DateTimeField): Data e hora da última atualização da conversa
    """
    OPEN_CHOICE = 'OPEN'
    CLOSED_CHOICE = 'CLOSED'
    STATES = (
        (OPEN_CHOICE, 'Open'),
        (CLOSED_CHOICE, 'Closed'),
    )
    
    id = models.UUIDField(primary_key=True)
    state = models.CharField(max_length=6, choices=STATES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} ({self.state})"


class Message(models.Model):
    """
    Modelo que representa uma mensagem dentro de uma conversa.
    
    Attributes:
        id (UUIDField): Identificador único da mensagem
        conversation (ForeignKey): Referência à conversa à qual a mensagem pertence
        direction (CharField): Direção da mensagem (SENT ou RECEIVED)
        content (TextField): Conteúdo da mensagem
        timestamp (DateTimeField): Data e hora do envio/recebimento da mensagem
        created_at (DateTimeField): Data e hora de criação do registro
    """
    SENT_CHOICE = 'SENT'
    RECEIVED_CHOICE = 'RECEIVED'
    DIRECTIONS = (
        (SENT_CHOICE, 'Sent'),
        (RECEIVED_CHOICE, 'Received'),
    )
    
    id = models.UUIDField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    direction = models.CharField(max_length=8, choices=DIRECTIONS)
    content = models.TextField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direction} message in conversation {self.conversation.id}"

    class Meta:
        ordering = ['timestamp']
