import threading
from time import sleep
#import requests
import socket
import json
from . import util
from random import random

encoder = json.JSONEncoder()

class Pacientes_threads: # objeto que é responsavle por gerir as threds dos dispostivos, que ficaram enviando periodicamente os dados dos sensores
    def __init__(self, ip:str,port:int, quais_dados:list, tempo_de_espera_para_envio_em_segundos:float):
        self.semafaros = {} # semafaros para podermos "matar" as threds
        self.adr = (ip,port) #ip e porta do servidor, servidor que se comunica com a interfacie do medico
        self.quais_dados = quais_dados# quais os campos que devem ser enviados
        self.intervalo_de_envio = tempo_de_espera_para_envio_em_segundos # quan o intervalo de tempo em segundos que o envio deve acontecer

    def add_paciente(self, nome:str, informações:list) -> None:
        '''
        Função para adição de um novo dispositivo, ira inicia uma thread que enviara periodicamente os dados nela salvos
        '''
        dados = {} # dados da thread
        for a,b in zip(self.quais_dados,informações): # salvamos os dados que a thread esta enviado
            dados[a]=b
        self.semafaros[nome] = threading.Semaphore(1) # salvamos o semafaro usado para "matar" a thread
        self.semafaros[nome].acquire() # travamos o semafaro para "matar" a thread no release
        threading.Thread(target=paciente_ação_socket, args=(nome,dados,self.semafaros[nome],self.adr,self.intervalo_de_envio), daemon=True).start() # criamos e iniciamos a thread
        
    def remover_paciente(self, nome:str) ->None:
        '''
        função para remoção de dispostivo
        '''
        do_delete_of_data(self.adr,nome)  #deletamos desse sistema
        self.semafaros[nome].release()# soltamso o semafaro para "matar" a thread
        del(self.semafaros[nome]) # deletamos os dados do dispostivo do sistema

def paciente_ação_socket(nome:str,dados:dict,semafaro:threading.Semaphore,adr:tuple,time:float) -> None:
    '''
    função que é executada na thred que envia constantemente os dados do dispostivo
    '''
    while True:
        try:
            do_post_put_of_data(adr,nome,dados,'POST')    #fazemos o envio dos dados na porta recebida pelo servidor
            break
        except:# caso hava algum erro tentaremos novamente, printa que nao foi poscivel enviar tal mensagem
            sleep(round(random(),2))
    sleep(time)#Esperamos o tempo determinado para atualiza os dados do dispositivo no servidor
    while True:
        if(semafaro.acquire(False)):# se o semafaro estiver bloqueado podemos proseguir
            break # mas caso esteja livre quebramos o loop
        try:
            do_post_put_of_data(adr,nome,dados,'PUT')    #fazemos o envio dos dados na porta recebida pelo servidor
            sleep(time)#caso tenhamos enviado a mensagem espera alguns instantes para enviar novamente
        except:# caso hava algum erro tentaremos novamente, printa que nao foi poscivel enviar tal mensagem
            sleep(round(random(),2))

def do_post_put_of_data(adr:tuple,nome:str,data:dict,action:str) -> None:
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
    s.send( get_mensagem(action,msg) )# enviamos a mensagem como string de bytes, sendo o json.JSONEncoder.encode dos dados
    s.close() #fechamos a conecção com o socket

def do_delete_of_data(adr:tuple,nome:str)->None:
    '''
    Faz o request de deletar um dispostivo do servidor
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# cria o socket para conecção
    s.settimeout(60)# caso demore 60 esperando para a conecção ser aceita ou tentando ler dados gera um erro
    s.connect(adr)# tentamos nos conectar ao servidor
    msg = {"paciente":nome} # mensagem que sera enviada
    s.send( get_mensagem('DELETE',msg) )# enviamos a mensagem como string de bytes, sendo o json.JSONEncoder.encode dos dados
    resp = util.read_from_socket(s,64)
    #print(f'deletado: {nome}')
    s.close()#fechamos a conecção com o socket

def get_mensagem(action:str,data:dict) -> bytes:
    msg = {'action':action,'headers':data}
    msg = util.padding_mensage( msg )
    return msg