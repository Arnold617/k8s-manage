from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path, re_path
from app.view.k8s_ssh import SSHConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('webSsh/', SSHConsumer.as_asgi()),
        ])
    ),
})