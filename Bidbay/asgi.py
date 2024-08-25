"""
ASGI config for Bidbay project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from Bidbay1.routing import wsPattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bidbay.settings')

# http_response_app = 

# application = get_asgi_application()

application=ProtocolTypeRouter(
    # {"http": get_asgi_application(), "websocket": URLRouter(wsPattern)}
    {"http": get_asgi_application(), "websocket": URLRouter(wsPattern)}
)
