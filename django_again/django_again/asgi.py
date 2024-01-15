"""
ASGI config for django_again project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chat.routing
import tictactoe.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_again.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([*chat.routing.websocket_urlpatterns, *tictactoe.routing.websocket_urlpatterns])
        )
    )
    # Just HTTP for now. (We can add other protocols later.)
})