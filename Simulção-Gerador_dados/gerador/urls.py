'''
Arquivo que vem com o django
'''
from django.conf.urls import url
from .views import add_paciente,remove_paciente,editar_paciente

app_name = "gerador"

urlpatterns = [ # urls usadas internamente para edição,remoção e adição de pacientes
    url(r'^add/$', add_paciente, name="add_paciente"),
    url(r'^remover/(?P<nome>[a-zA-Z0-9]+)/$', remove_paciente, name="remover_paciente"),
    url(r'^editar/(?P<nome>[a-zA-Z0-9]+)/$', editar_paciente, name="editar_paciente"),
]