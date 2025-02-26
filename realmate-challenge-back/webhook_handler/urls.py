from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebhookViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'webhooks', WebhookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]