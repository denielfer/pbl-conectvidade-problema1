'''
    ARQUIVO DJANGO PARA ESTABELECER ROTAS
'''
from django.urls import path
from django.conf.urls import url
from .views import show_data

app_name = "receptor"

urlpatterns = [
    url(r'^$', show_data, name="list_pacients"), # rota raiz sera a de mostra pacientes
]