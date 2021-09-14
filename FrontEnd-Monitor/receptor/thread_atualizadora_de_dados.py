from . import socke_handler
from time import sleep
import requests
from threading import Thread

ip = "26.181.221.42" #ip da maquina que esta rodando a API
port = 5000 #porta base para a API

class dados:
    is_server_on = False
    lista_dados_por_paciente = None

dados_salvos = dados()
def __get_pacientes__():
    '''
    Função que determina como os dados serão obtidos, se por socket ou pela API

    @return dicitionario contendo os dados do pacientes
    @raise Socket_Exceptions se qualquer problema acontecer com a coneção, para o caso de ser feita atravez de sockets
    '''
    pacients = socke_handler.get_dados() # tenta pegar dados do sistema atravez do socekt
    # pacients = requests.get(f"http://{ip}:{port}/").json() # tenta pega dados do sistema atravez da API
    return pacients

def update_pacientes(DADOS_FROM_DEVICE:list,Tempo_de_espera_s:float):
    '''
        Funçao para thread que ficara atualizando pacientes

        @param DADOS_FROM_DEVICE, lista contendo as chaves dos dados que serao procurados no dicionario de pacientes enviado pelo servidor
        @param Tempo_de_espera_s, float indicando de quanto em quanto tempo se atualizara os dados
    '''
    while True:
        try:
            pacients = __get_pacientes__() # chama função que traz os dadados pro sistema
            #criamos variaveis que serao usadas pelo django para monta o html
            lista_nomes = [a for a in pacients] # temos a lista de nomes dos pacientes
            lista_dados_por_paciente_t = [ (b,[pacients[b][a] for a in DADOS_FROM_DEVICE]) for b in lista_nomes ] # montamos a lista de pacientes e dados
            lista_dados_por_paciente_t.sort(reverse=True,key=lambda x:x[1][4]) # oredenamos a lista de pacientes
            dados_salvos.lista_dados_por_paciente = lista_dados_por_paciente_t
            dados_salvos.is_server_on = True
        except ConnectionRefusedError: # caso haja erro carregamos um html para informa que nao foi poscivel se conectar ao seridor
            dados_salvos.is_server_on = False
        sleep(Tempo_de_espera_s)

def init_thread_update_pacientes(DADOS_FROM_DEVICE:list,Tempo_de_espera_s:float):
    '''
        Funçao que cria e inicia a thread de atualizar os dados do paciente no servidor

        @param DADOS_FROM_DEVICE, lista contendo as chaves dos dados que serao procurados no dicionario de pacientes enviado pelo servidor
        @param Tempo_de_espera_s, float indicando de quanto em quanto tempo se atualizara os dados
    '''
    t = Thread(target=update_pacientes,args=(DADOS_FROM_DEVICE,Tempo_de_espera_s))
    t.setDaemon(True)
    t.start()

def get_is_server_on() -> bool:
    '''
        Função que retorna se a ultima conexão com o server foi bem sucedida

        @return bool que indica se a ultima conexão com o server foi bem sucedida ( ou seja se ele esta online)
    '''
    return dados_salvos.is_server_on

def get_dados():
    '''
        Função que retorna os dados dos pacientes ondenados por prioridade
        os dados estao na seguinte estrutura:
        [(__identificador_do_paciente__,__dados_do_paciente__),...]

        @return list contendo o nome dos pacientes e seus dados em uma tupla
    '''
    return dados_salvos.lista_dados_por_paciente