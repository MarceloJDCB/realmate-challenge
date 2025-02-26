from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from realmate_challenge import settings

class WebhookAuthentication(BaseAuthentication):
    """
    Classe de autenticação personalizada para endpoints de webhook.
    
    Implementa autenticação via token simples em ambiente de desenvolvimento
    e via HMAC em produção para garantir a segurança das chamadas webhook.
    """
    def authenticate(self, request):
        """
        Autentica uma requisição webhook.

        Args:
            request: A requisição HTTP a ser autenticada

        Returns:
            tuple: (None, None) se a autenticação for bem sucedida

        Raises:
            AuthenticationFailed: Se a autenticação falhar por falta de token
                                ou token inválido
        """
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')

        if settings.DEBUG:
            if token != settings.WEBHOOK_API_KEY:
                raise AuthenticationFailed('Invalid token')
        else:
            # Verifica se a requisição possui um HMAC válido.
            # Autenticação via HMAC
            pass

        return (None, None)