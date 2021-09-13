from django.http import HttpResponse
from django.template import loader
from . import socke_handler
import requests

REFRESH_TIME_IN_MS = 1*1000 # de quanto em quanto tempo atualizaremos os dados na interfacie
DADOS_FROM_DEVICE=["pressão","oxigenação","frequencia","temperatura","prioridade"] # quais os dados sao esperados que o dispositivo tenha

ip = "26.181.221.42" #ip da maquina que esta rodando a API
port = 5000 #porta base para a API

def get_pacientes():
    '''
    Função que determina como os dados serão obtidos, se por socket ou pela API

    @return dicitionario contendo os dados do pacientes
    '''
    pacients = socke_handler.get_dados() # tenta pegar dados do sistema atravez do socekt
    # pacients = requests.get(f"http://{ip}:{port}/").json() # tenta pega dados do sistema atravez da API
    return pacients

def show_data(request):
    '''
    Função que recebe o request e retorna a pagina com dados de todos os pacientes

    @param request: request http para a pagina
    @return: django.http.HttpResponse contendo a pagina renderizada
    '''
    try:
        pacients = get_pacientes() # chama função que traz os dadados pro sistema
        template = loader.get_template("pacients_list.html") #carega o arquivo html que sera enviado como resposta
        #criamos variaveis que serao usadas pelo django para monta o html
        lista_nomes = [a for a in pacients] # temos a lista de nomes dos pacientes
        lista_dados_por_paciente = [ (b,[pacients[b][a] for a in DADOS_FROM_DEVICE]) for b in lista_nomes ] # montamos a lista de pacientes e dados
        lista_dados_por_paciente.sort(reverse=True,key=lambda x:x[1][4]) # oredenamos a lista de pacientes
        context = { 'nomes_dado':lista_dados_por_paciente, 'campos':DADOS_FROM_DEVICE, 'tempo_espera':REFRESH_TIME_IN_MS } #dicionario que guarda os dadso passados para a renderização da pagina
        return HttpResponse(template.render(context,request)) # retornamos os html criado
    except: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))

def show_data_in_page(request,num_pagina,num_pacientes):
    '''
    Função que recebe o request e retorna a pagina com dados de alguns pacientes os pacientes em uma dada pagina

    @param request: request http para a pagina
    @param num_pagina: int representando qual a pagina que sera retornada
    @param num_pacientes: int, numero de pacientes por pagina
    @return: django.http.HttpResponse contendo a pagina renderizada
    '''
    try:
        pacients = get_pacientes() # chama função que traz os dadados pro sistema
        template = loader.get_template("alguns_pacientes.html") #carega o arquivo html que sera enviado como resposta
        #criamos variaveis que serao usadas pelo django para monta o html
        lista_nomes = [a for a in pacients] #lista de nomes dso pacientes
        pacientes_por_pagina = num_pagina*num_pacientes # posição do primeiro paciente da pagina ( pagina * numero do paciente )
        lista_dados_por_paciente = [ (b,[pacients[b][a] for a in DADOS_FROM_DEVICE]) for b in lista_nomes ] # lista de dados por paciente
        lista_dados_por_paciente.sort(reverse=True,key=lambda x:x[1][4]) # arumamos a lista
        lista_filtrados = lista_dados_por_paciente[pacientes_por_pagina:pacientes_por_pagina+num_pacientes] # filtramos a lista para devolver apenas a quantidade de pacientes solicidados começando no primiero paciente da pagina
        #dicionario que guarda os dadso passados para a renderização da pagina
        context = { 'nomes_dado':lista_filtrados, 
                    'campos':DADOS_FROM_DEVICE, 
                    'tempo_espera':REFRESH_TIME_IN_MS,
                    "num_pacientes":num_pacientes,
                    "tem_proxima_pagina":(len(lista_dados_por_paciente[pacientes_por_pagina+num_pacientes:pacientes_por_pagina+2*num_pacientes]) > 0), 
                    "tem_pagina_anterior":(len(lista_dados_por_paciente[pacientes_por_pagina-num_pacientes:pacientes_por_pagina]) > 0),
                    "proxima_pagina":num_pagina+1,
                    "pagina_anterior":num_pagina-1,
                    "num_pagina":num_pagina+1}
        return HttpResponse(template.render(context,request)) # retornamos os html criado
    except: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))

def show_paciente(request,paciente_nome):
    '''
    Função que recebe o request e retorna uma pagina com os dados do paciente especificado

    @param paciente_nome: str contendo o nome do paciente que sera procurado
    @return: django.http.HttpResponse contendo a pagina renderizada
    '''
    try:
        pacients = get_pacientes() # chama função que traz os dadados pro sistema
        try:
        #     print(paciente_nome)
        #     print([a for a in pacients])
            paciente = pacients[paciente_nome]#tentanmos pegar o dado do paciente especificado
            template = loader.get_template("paciente.html") #carega o arquivo html que sera enviado como resposta
            context = { #dicionario que guarda os dadso passados para a renderização da pagina
                'dados':zip(['Nome']+DADOS_FROM_DEVICE,[paciente_nome]+[paciente[tipo] for tipo in DADOS_FROM_DEVICE]),
                'tempo_espera':REFRESH_TIME_IN_MS,
            }
            return HttpResponse(template.render(context,request)) # retornamos os html criado
        except: # caso o paciente nao seja encontrado
            template = loader.get_template("paciente_nao_encontrado.html") #caregamos o html de paciente nao encontrado
            return HttpResponse(template.render({},request))#enviamos a resposta
    except: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))