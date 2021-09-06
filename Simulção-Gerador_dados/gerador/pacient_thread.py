import threading
from time import sleep
#import requests
import socket
import json
from . import util

encoder = json.JSONEncoder()

class Pacientes_threads: # objeto que é responsavle por gerir as threds dos dispostivos, que ficaram enviando periodicamente os dados dos sensores
    def __init__(self, ip,port, quais_dados, tempo_de_espera_para_envio_em_segundos):
        self.semafaros = {} # semafaros para podermos "matar" as threds
        self.adr = (ip,port) #ip e porta do servidor, servidor que se comunica com a interfacie do medico
        self.quais_dados = quais_dados# quais os campos que devem ser enviados
        self.intervalo_de_envio = tempo_de_espera_para_envio_em_segundos # quan o intervalo de tempo em segundos que o envio deve acontecer

    def add_paciente(self, nome, informações):
        '''
        Função para adição de um novo dispositivo, ira inicia uma thread que enviara periodicamente os dados nela salvos
        '''
        dados = {} # dados da thread
        for a,b in zip(self.quais_dados,informações): # salvamos os dados que a thread esta enviado
            dados[a]=b
        self.semafaros[nome] = threading.Semaphore(1) # salvamos o semafaro usado para "matar" a thread
        self.semafaros[nome].acquire() # travamos o semafaro para "matar" a thread no release
        threading.Thread(target=paciente_ação_socket, args=(nome,dados,self.semafaros[nome],self.adr,self.intervalo_de_envio), daemon=True).start() # criamos e iniciamos a thread
        
    def remover_paciente(self, nome):
        '''
        função para remoção de dispostivo
        '''
        port = get_port_to_action("DELETE",self.adr)# pegamos a porta que devemos nos comunicar para deletar o dispositvo do servidor, servidor que se comunica com a interfacie do medico
        do_delete_of_data((self.adr[0],port),nome)  #deletamos desse sistema
        self.semafaros[nome].release()# soltamso o semafaro para "matar" a thread
        del(self.semafaros[nome]) # deletamos os dados do dispostivo do sistema

def paciente_ação_socket(nome,dados,semafaro,adr,time):
    '''
    função que é executada na thred que envia constantemente os dados do dispostivo
    '''
    while True:
        if(semafaro.acquire(False)):# se o semafaro estiver bloqueado podemos proseguir
            break # mas caso esteja livre quebramos o loop
        try:
            port = get_port_to_action("POST",adr) # tentamos conseguir uma porta para enviar os dados
            do_post_put_of_data((adr[0],port),nome,dados)    #fazemos o envio dos dados na porta recebida pelo servidor
        except:# caso hava algum erro tentaremos novamente, printa que nao foi poscivel enviar tal mensagem
            print(f"falha no envio {nome}")
            sleep(.2)
            continue
        sleep(time)#caso tenhamos enviado a mensagem espera alguns instantes para enviar novamente

def get_port_to_action(action,adr):
    '''
    Função que se comunica com o servidor para conseguir uma prota para realizar a ação passada

    @param action: "POST","GET","PUT" or "DELETE", sendo a ação desejada
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#criamos o socket
    s.settimeout(60) # caso demore 60 esperando para a conecção ser aceita ou tentando ler dados gera um erro
    s.connect(adr)# tentamos nos conectar ao servidor
    s.send(bytes(encoder.encode({'action':action}), 'utf-8'))#enviamos o pedido para realizar a ação passada
    resp = util.read_from_socket(s)# lemos a resposta
    s.close()#fechamos os socket
    return resp['data']["port"]# retornamos a resposta do servidor

def do_post_put_of_data(adr,nome,data):
    '''
    Função que reliza o envio de dados de um dispositivo para o sistema, sendo um envio do tipo "POST" ou "PUT"

    @param adr, tupla contendo o ip em string e a porta em inteiro, que se tentara a conecção com o servidor
    @param nome, str sendo o identificador do paciente, nome do paciente que os dados entao sendo enviadoss
    @param data, dicionario contendo os dados dos sensores do dispositvo que serao enviados
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# cria o socket para conecção
    s.settimeout(60) # caso demore 60 esperando para a conecção ser aceita ou tentando ler dados gera um erro
    s.connect(adr)# tentamos nos conectar ao servidor
    msg = {"paciente":nome,"dados":data} # mensagem que sera enviada
    #print(msg)
    s.send(bytes(encoder.encode(msg), 'utf-8'))# enviamos a mensagem como string de bytes, sendo o json.JSONEncoder.encode dos dados
    s.close() #fechamos a conecção com o socket

def do_delete_of_data(adr,nome):
    '''
    Faz o request de deletar um dispostivo do servidor
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# cria o socket para conecção
    s.settimeout(60)# caso demore 60 esperando para a conecção ser aceita ou tentando ler dados gera um erro
    s.connect(adr)# tentamos nos conectar ao servidor
    msg = {"paciente":nome} # mensagem que sera enviada
    s.send(bytes(encoder.encode(msg), 'utf-8'))# enviamos a mensagem como string de bytes, sendo o json.JSONEncoder.encode dos dados
    print(f'deletado: {nome}')
    s.close()#fechamos a conecção com o socket