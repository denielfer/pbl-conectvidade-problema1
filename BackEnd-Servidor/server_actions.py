import threading
import util
from time import sleep
import json

pickle = json.JSONEncoder()

def server_socket_sensor_start(pacientes,sokt):
    '''
    Função que cria uma thread para lidar cm requests PUT e POST 

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    threading.Thread(target=socket_sensor_action,  args=(pacientes,sokt)).start()

def socket_sensor_action(pacients,sokt):
    '''
    Função da thread para os sockets de POST e PUT

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    # A PRIMIERA MENSAGEM DEVE CONTER {"lenght":length_da_proxima_mensagem} 
    # o que por padrao deixa com 512-27=485 bytes para o inteiro representando
    # {length_da_proxima_mensagem}
    while True:
        try:
            (clientsocket, address) = sokt.accept()
            msg = util.read_from_socket(clientsocket,length=1024)
#        resp = {"status":400}
            #print(f'atualizando: {msg["paciente"]}, dados: {msg["dados"]}')
            pacients[msg["paciente"]] = msg["dados"]
            pacients[msg["paciente"]]["is_critical"] = check_if_prioridade(msg["dados"])
#            resp["status"]=200
        except:
            pass
#        resp = util.padding_mensage( pickle.encode(resp) )
#        clientsocket.send(bytes(resp, 'utf-8'))
        sleep(.001)

def server_socket_get_start(pacientes,sokt):
    '''
    Função que cria uma thread para lidar cm requests GET 

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    threading.Thread(target=socket_get_action, args=(pacientes,sokt)).start()

def socket_get_action(pacientes,sokt):
    '''
    Função da thread para os sockets de GET

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    while True:
        try:
            (clientsocket, address) = sokt.accept()
            #print("aceito")
            msg = pickle.encode(pacientes)
            #print("encoded")
            clientsocket.send( util.padding_mensage(len(msg) ) )
            #print("enviando length")
            clientsocket.send( bytes(msg, 'utf-8'))
            #print("enviando dados")
        except:
            pass
        sleep(.001)

def server_socket_delete_start(pacientes,sokt):
    '''
    Função que cria uma thread para lidar cm requests DELETE

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    threading.Thread(target=socket_sensor_delete,  args=(pacientes,sokt)).start()

def socket_sensor_delete(pacients,sokt):
    '''
    Função da thread para os sockets de DELETE

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    # A PRIMIERA MENSAGEM DEVE CONTER {"lenght":length_da_proxima_mensagem} 
    # o que por padrao deixa com 512-27=485 bytes para o inteiro representando
    # {length_da_proxima_mensagem}
    while True:
        try:
            (clientsocket, address) = sokt.accept()
            msg = util.read_from_socket(clientsocket,length=1024)
            del(pacients[msg["paciente"]])
        except:
            pass

def check_if_prioridade(dados_do_paciente):
    '''
    Verifica se o paciente esta em estado critico com base nos dados

    @param dados_do_pacient, dicionario, com os dados do pacientes

    Esses dados devem conter: 
        "preção", que representa a preção maxima medida deve ser um int, 
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
    if (dados_do_paciente["preção"]<100):
        cont+=1
    if(dados_do_paciente["oxigenação"]<96):
        cont+=1
    if(dados_do_paciente["frequencia"]>20):
        cont+=1
    if(dados_do_paciente["temperatura"]>38.0):
        cont+=1
    return cont == 0