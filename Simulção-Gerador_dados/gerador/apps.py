'''
Arquivo que vem com o django
'''
from django.apps import AppConfig

class GeradorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gerador'
