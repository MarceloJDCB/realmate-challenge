import hmac
import hashlib

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from realmate_challenge import settings

class WebhookAuthentication(BaseAuthentication):
    """
    Autenticação personalizada para webhooks baseada em HMAC.

    Esta classe implementa um mecanismo de autenticação para webhooks usando HMAC-SHA256.
    Em modo de desenvolvimento (DEBUG=True), verifica apenas a correspondência direta com WEBHOOK_API_KEY.
    Em produção, verifica a assinatura HMAC do corpo da requisição usando WEBHOOK_SECRET.

    Raises:
        AuthenticationFailed: Se a assinatura estiver ausente, inválida, ou se o corpo da requisição estiver vazio.

    Returns:
        tuple: (None, None) se a autenticação for bem-sucedida.
    """
    def authenticate(self, request):
        received_signature = request.headers.get('Authorization')
        if not received_signature:
            raise AuthenticationFailed('No signature provided')

        if not request.body:
            raise AuthenticationFailed('Empty request body')

        if settings.DEBUG:
            # Modo desenvolvimento: ainda usando compare_digest para segurança
            if not hmac.compare_digest(
                received_signature.encode('utf-8'), 
                settings.WEBHOOK_API_KEY.encode('utf-8')
            ):
                raise AuthenticationFailed('Invalid token')
        else:
            if not received_signature.startswith('HMAC '):
                raise AuthenticationFailed('Invalid signature format')
            
            received_signature = received_signature.split(' ')[1]
            
            secret_key = settings.WEBHOOK_SECRET.encode('utf-8')
            expected_signature = hmac.new(
                secret_key,
                msg=request.body,
                digestmod=hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, received_signature):
                raise AuthenticationFailed('Invalid HMAC signature')

        return (None, None)