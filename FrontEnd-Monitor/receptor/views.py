from typing import ContextManager
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from . import socke_handler

REFRESH_TIME_IN_MS = 1*1000
DADOS_FROM_DEVICE=["preção","oxigenação","frequencia","temperatura"]

def show_data(request):
    try:
        #print("geting data")
        pacients = socke_handler.get_dados()
        template = loader.get_template("pacients_list.html")
        #print("using data")
        lista_nomes = [a for a in pacients]
        #print("dfc1")
        lista_dados_por_paciente = [ [pacients[b][a] for a in DADOS_FROM_DEVICE] for b in lista_nomes ]
        context = { 'nomes_dado':zip(lista_nomes,lista_dados_por_paciente), 'campos':DADOS_FROM_DEVICE, 'tempo_espera':REFRESH_TIME_IN_MS }
        return HttpResponse(template.render(context,request))
    except ConnectionRefusedError:
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))
