import threading
from time import sleep
#import requests
import socket
import json
from . import util

encoder = json.JSONEncoder()

class Pacientes_threads:
    def __init__(self, ip,port, quais_dados, tempo_de_espera_para_envio_em_segundos):
        self.semafaros = {}
        self.adr = (ip,port)
        self.quais_dados = quais_dados
        self.intervalo_de_envio = tempo_de_espera_para_envio_em_segundos

    def add_paciente(self, nome, informações):
        dados = {}
        for a,b in zip(self.quais_dados,informações):
            dados[a]=b
        self.semafaros[nome] = threading.Semaphore(1)
        self.semafaros[nome].acquire()        
        threading.Thread(target=paciente_ação_socket, args=(nome,dados,self.semafaros[nome],self.adr,self.intervalo_de_envio)).start()
        
    def remover_paciente(self, nome):
        port = get_port_to_action("DELETE",self.adr)
        do_delete_of_data((self.adr[0],port),nome)  
        self.semafaros[nome].release()
        del(self.semafaros[nome])

def paciente_ação_socket(nome,dados,semafaro,adr,time):
    while True:
        if(semafaro.acquire(False)):
            break
        #print(nome,"  enviado")
        try:
            port = get_port_to_action("POST",adr)
            do_post_put_of_data((adr[0],port),nome,dados)    
        except:
            print(f"falha no envio {nome}")
            continue
        sleep(time)

def get_port_to_action(action,adr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(adr)
    s.send(bytes(encoder.encode({'action':action}), 'utf-8'))
    resp = util.read_from_socket(s)
    return resp["port"]

def do_post_put_of_data(adr,nome,data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(adr)
    msg = {"paciente":nome,"dados":data}
    #print(msg)
    s.send(bytes(encoder.encode(msg), 'utf-8'))
    s.close()

def do_delete_of_data(adr,nome):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(adr)
    msg = {"paciente":nome}
    s.send(bytes(encoder.encode(msg), 'utf-8'))
    print(f'deletado: {nome}')
    s.close()










    
# def paciente_ação(nome, dados,url_base,time,semafaro):  
#     while True:
#         if(semafaro.acquire(False)):
#             break
#         print(nome,"  enviado", end=' ')
#         try:
#             requests.post( f"{url_base}/set_dado/{nome}/", data=dados )
#         except requests.exceptions.ConnectionError:
#             print("falha no envio")
#         except :
#             pass
#         print()
#         sleep(time)