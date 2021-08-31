from typing import ContextManager
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import comunicação

def show_data(request):
    try:
        pacients = comunicação.get_dados()
        template = loader.get_template("pacients_list.html")
        lista_nomes = [a for a in pacients]
        try:
            lista_campos = [a for a in pacients[lista_nomes[0]]]
        except IndexError:
            lista_campos = []
        lista_dados_por_paciente = [ [pacients[b][a] for a in lista_campos] for b in lista_nomes ]
        context = { 'nomes_dado':zip(lista_nomes,lista_dados_por_paciente), 'campos':lista_campos, 'tempo_espera':1000 }
        return HttpResponse(template.render(context,request))
    except TimeoutError:
        template = loader.get_template("server_of_line.html")
        return HttpResponse(template.render({},request))
