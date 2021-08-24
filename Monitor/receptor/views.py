from typing import ContextManager
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json
# Create your views here.
import gzip

pacients = {}

@csrf_exempt
def recive_data(request,id):
    '''
    This function deals with the reception of pacient's data
    it will recive and storage the date to be showed 
    '''
    if(request.method == 'POST'): 
        msg = request.POST #pegamos os dados passados em binario
        pacients[id] = msg
        print(id)
    else:
        print('get')
    return JsonResponse({},safe=True)

def show_data(request):
    template = loader.get_template("pacients_list.html")
    lista_nomes = [a for a in pacients]
    try:
        lista_campos = [a for a in pacients[lista_nomes[0]]]
    except IndexError:
        lista_campos = []
    lista_dados_por_paciente = [ [pacients[b][a] for a in lista_campos] for b in lista_nomes ]
    context = { 'nomes_dado':zip(lista_nomes,lista_dados_por_paciente), 'campos':lista_campos, 'tempo_espera':1000 }
    return HttpResponse(template.render(context,request))
