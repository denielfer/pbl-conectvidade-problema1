from django.http import HttpResponse
from django.template import loader
from . import socke_handler

REFRESH_TIME_IN_MS = 1*1000 # de quanto em quanto tempo atualizaremos os dados na interfacie
DADOS_FROM_DEVICE=["preção","oxigenação","frequencia","temperatura","prioridade"] # quais os dados sao esperados que o dispositivo tenha

def show_data(request):
    try:
        #print("geting data")
        pacients = socke_handler.get_dados() # tenta pegar dados do sistema
        template = loader.get_template("pacients_list.html") #carega o arquivo html que sera enviado como resposta
        #print("using data")
        #criamos variaveis que serao usadas pelo django para monta o html
        lista_nomes = [a for a in pacients]
        #print("dfc1")
        lista_dados_por_paciente = [ [pacients[b][a] for a in DADOS_FROM_DEVICE] for b in lista_nomes ]
        lista_dados_por_paciente.sort(reverse=True,key=lambda x:x[4])
        context = { 'nomes_dado':zip(lista_nomes,lista_dados_por_paciente), 'campos':DADOS_FROM_DEVICE, 'tempo_espera':REFRESH_TIME_IN_MS }
        return HttpResponse(template.render(context,request)) # retornamos os html criado
    except ConnectionRefusedError: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":REFRESH_TIME_IN_MS},request))
