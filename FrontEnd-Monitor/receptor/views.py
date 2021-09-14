from django.http import HttpResponse
from django.template import loader
from . import thread_atualizadora_de_dados

REFRESH_TIME_IN_S = 1
REFRESH_TIME_IN_MS = REFRESH_TIME_IN_S*1000 # de quanto em quanto tempo atualizaremos os dados na interfacie
DADOS_FROM_DEVICE=["pressão","oxigenação","frequencia","temperatura","prioridade"] # quais os dados sao esperados que o dispositivo tenha

thread_atualizadora_de_dados.init_thread_update_pacientes(DADOS_FROM_DEVICE,REFRESH_TIME_IN_S)

def show_data(request):
    '''
    Função que recebe o request e retorna a pagina com dados de todos os pacientes

    @param request: request http para a pagina
    @return: django.http.HttpResponse contendo a pagina renderizada
    '''
    if thread_atualizadora_de_dados.get_is_server_on():
        lista_dados_por_paciente = thread_atualizadora_de_dados.get_dados() # caregamos os dados dos pacientes 
        template = loader.get_template("pacients_list.html") #carega o arquivo html que sera enviado como resposta
        context = { 'nomes_dado':lista_dados_por_paciente, 'campos':DADOS_FROM_DEVICE, 'tempo_espera':REFRESH_TIME_IN_MS } #dicionario que guarda os dadso passados para a renderização da pagina
        return HttpResponse(template.render(context,request)) # retornamos os html criado
    else: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
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
    if thread_atualizadora_de_dados.get_is_server_on():
        lista_dados_por_paciente = thread_atualizadora_de_dados.get_dados() # caregamos os dados dos pacientes 
        template = loader.get_template("alguns_pacientes.html") #carega o arquivo html que sera enviado como resposta
        pacientes_por_pagina = num_pagina*num_pacientes # posição do primeiro paciente da pagina ( pagina * numero do paciente )
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
    else: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))

def show_paciente(request,paciente_nome):
    '''
    Função que recebe o request e retorna uma pagina com os dados do paciente especificado

    @param paciente_nome: str contendo o nome do paciente que sera procurado
    @return: django.http.HttpResponse contendo a pagina renderizada
    '''
    if thread_atualizadora_de_dados.get_is_server_on():
        lista_dados_por_paciente = thread_atualizadora_de_dados.get_dados() # caregamos os dados dos pacientes 
        try:
            # aqui teremos uma lista com no maximo 1 paciente, pois o servidor que guarda os dados dos dispositivos de monitoramento os armazena em uma hashmap então ou esta lista esta vazia, caso o paciente nao exista, ou ela tem 1, 1 e apenas 1, elemento que é o paciente cuja identificação, que neste caso esta sendo usado o nome do paciente, foi passada
            paciente = [a for a in lista_dados_por_paciente if paciente_nome in a] 
            template = loader.get_template("paciente.html") #carega o arquivo html que sera enviado como resposta
            context = { #dicionario que guarda os dadso passados para a renderização da pagina
                'dados':zip(['Nome']+DADOS_FROM_DEVICE,[paciente[0][0]]+paciente[0][1]),# caso isso gera um erro é pois a lista nao tinha nenhum elemento ou seja o paciente nao existe no sistema, caso contrario ( ele existir ) so vai existir 1 elemento 
                'tempo_espera':REFRESH_TIME_IN_MS,
            }
            return HttpResponse(template.render(context,request)) # retornamos os html criado
        except: # caso o paciente nao seja encontrado
            template = loader.get_template("paciente_nao_encontrado.html") #caregamos o html de paciente nao encontrado
            return HttpResponse(template.render({},request))#enviamos a resposta
    else: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))