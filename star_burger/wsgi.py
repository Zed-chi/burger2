"""
WSGI config for qwe project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

# from django.core.wsgi import get_wsgi_application
from environs import Env

env = Env()
env.read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "star_burger.settings")
from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
