from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path("ws/justchat/", ChatConsumer.as_asgi()),
    path("ws/justchat/<str:chat_id>/", ChatConsumer.as_asgi()),

]
