import hmac
import hashlib

from rest_framework.throttling import SimpleRateThrottle
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, Throttled
from realmate_challenge import settings


class WebhookRateThrottle(SimpleRateThrottle):
    """
    Limitador de taxa de requisições para endpoints webhook.

    Limita as requisições a 60 por minuto por endereço IP para prevenir abusos.
    Usa o endereço IP do cliente como identificador único para limitação de taxa.
    """
    rate = '60/minute'
    scope = 'webhook'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


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

    def __init__(self):
        self.throttle = WebhookRateThrottle()

    def authenticate(self, request):
        # Verificar rate limiting primeiro
        if not self.throttle.allow_request(request, self):
            raise Throttled(detail="Too many requests")

        received_signature = request.headers.get('Authorization')
        if not received_signature:
            raise AuthenticationFailed('No signature provided')

        if request.method != "GET" and not request.body:
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
