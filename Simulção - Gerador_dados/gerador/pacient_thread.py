import threading
from time import sleep
import requests

class pacientes_threads:
    def __init__(self, url, quais_dados, tempo_de_espera_para_envio_em_segundos):
        self.semafaros = {}
        self.base_url = url
        self.quais_dados = quais_dados
        self.intervalo_de_envio = tempo_de_espera_para_envio_em_segundos

    def add_paciente(self, nome, informações):
        dados = {}
        for a,b in zip(self.quais_dados,informações):
            dados[a]=b
        self.semafaros[nome] = threading.Semaphore(1)
        self.semafaros[nome].acquire()        
        threading.Thread(target=paciente_ação, args=(nome,dados,self.base_url,self.intervalo_de_envio,self.semafaros[nome])).start()
        
    def remover_paciente(self, nome):
        self.semafaros[nome].release()
        del(self.semafaros[nome])

def paciente_ação(nome, dados,url_base,time,semafaro):
    while True:
        if(semafaro.acquire(False)):
            break
        print(nome,"  enviado", end=' ')
        try:
            requests.post( f"{url_base}/set_dado/{nome}/", data=dados )
        except requests.exceptions.ConnectionError:
            print("falha no envio")
        except :
            pass
        print()
        sleep(time)