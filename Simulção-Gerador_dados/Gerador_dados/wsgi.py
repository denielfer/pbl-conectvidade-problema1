'''
Arquivo que vem com o django
'''
"""
WSGI config for Gerador_dados project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gerador_dados.settings')

application = get_wsgi_application()
