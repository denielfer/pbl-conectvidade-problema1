import util
from time import sleep
import json
import socket

pickle = json.JSONEncoder()

def socket_sensor_action(pacients:dict,sokt:socket,msg:dict) -> None:
    '''
    Função da thread para lida com POST e PUT

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    @param msg dicionario sendo o header da mensagem enviada pelo cliente
    '''
    try:
        pacients[msg["paciente"]] = msg["dados"] # tentamos salvar os dados que ele enviou
        pacients[msg["paciente"]]["prioridade"] = check_if_prioridade(msg["dados"]) # salvamos se a situação do paciente é critica ou nao, salvando o nivel da sua prioridade
    except: # caso hava ecessao foi por envio erado do client
        sokt.close()

def socket_get_action(pacientes:dict,sokt:socket,adr:tuple) -> None:
    '''
    Função da thread para os sockets de GET

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    @param msg dicionario sendo o header da mensagem enviada pelo cliente
    '''
    try:
        sleep(.01)
        msg = pickle.encode(pacientes) # serealizamos os dados a serem enviados
        sokt.sendto( util.padding_mensage(len(msg),128 ),adr ) # enviamos o tamanho da proxima mensagem que contera os dadso serealizados
        sokt.sendto( bytes(msg, 'utf-8'),adr) # enviamos os dados serealizados
    except:
        sokt.close()

def socket_sensor_delete(pacients:dict,sokt:socket,msg:dict) -> None:
    '''
    Função da thread para os sockets de DELETE

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    @param msg dicionario sendo o header da mensagem enviada pelo cliente
    '''
    try:
        del(pacients[msg["paciente"]]) # tentamos remover o paciente informado
    except:
        sokt.close()

def check_if_prioridade(dados_do_paciente:dict) -> int:
    '''
    Verifica se o paciente esta em estado critico com base nos dados

    @param dados_do_pacient, dicionario, com os dados do pacientes

    Esses dados devem conter: 
        "pressão", que representa a pressão maxima medida deve ser um int, 
            é considerado critico se menor que 100, 
        "oxigenação", int representando a % de oxigenação no sangue, 
            critico se menor que 96
        "frequencia", int indicando a frequencia respiratoria, sendo 
            a quantidade de inspirações e expirações em um miuto , 
            critico se maior que 20
        "temperatura", float indicando a temperatura do corpo, critico
            se maior que 38 
    '''
    cont = 0
    if (dados_do_paciente["pressão"]<100):
        cont+=1
    if(dados_do_paciente["oxigenação"]<96):
        cont+=1
    if(dados_do_paciente["frequencia"]>20):
        cont+=1
    if(dados_do_paciente["temperatura"]>38.0):
        cont+=1
    return cont