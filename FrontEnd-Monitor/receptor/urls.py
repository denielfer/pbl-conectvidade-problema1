'''
    ARQUIVO DJANGO PARA ESTABELECER ROTAS
'''
from django.urls import path
from django.conf.urls import url
from .views import show_data,show_data_in_page,show_paciente

app_name = "receptor"

urlpatterns = [
    url(r'^$', show_data, name="list_pacients"), # rota raiz sera a de mostra todos pacientes
    path('<int:num_pagina>/<int:num_pacientes>/', show_data_in_page, name="list_pacients_por_numero"), # rota para mostra pacientes de x em x
    path('<slug:paciente_nome>/', show_paciente, name="paciente"), # rota para mostra pacientes de x em x
]