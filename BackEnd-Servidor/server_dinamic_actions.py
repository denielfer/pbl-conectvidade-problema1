import util
from time import sleep
import json

pickle = json.JSONEncoder()

def socket_sensor_action(pacients,sokt):
    '''
    Função da thread para os sockets de POST e PUT

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    # A PRIMIERA MENSAGEM DEVE CONTER {"lenght":length_da_proxima_mensagem} 
    # o que por padrao deixa com 512-27=485 bytes para o inteiro representando
    # {length_da_proxima_mensagem}
    try:
        (clientsocket, address) = sokt.accept()# aceitamos a conecção do cliente
        msg = util.read_from_socket(clientsocket,length=1024) # lemos a mensagem que ele enviou
#        resp = {"status":400}
        #print(f'atualizando: {msg["paciente"]}, dados: {msg["dados"]}')
        pacients[msg["paciente"]] = msg["dados"] # tentamos salvar os dados que ele enviou
    except: # caso hava ecessao foi por envio erado do client
        return
    pacients[msg["paciente"]]["prioridade"] = check_if_prioridade(msg["dados"]) # salvamos se a setuação do paciente é critica ou nao, salvando o nivel da sua preferencia
#            resp["status"]=200
#        resp = util.padding_mensage( pickle.encode(resp) )
#        clientsocket.send(bytes(resp, 'utf-8'))

def socket_get_action(pacientes,sokt):
    '''
    Função da thread para os sockets de GET

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    try:
        (clientsocket, address) = sokt.accept() # aceitamos a conecção
        #print("aceito")
        msg = pickle.encode(pacientes) # serealizamos os dados a serem enviados
        #print("encoded")
        clientsocket.send( util.padding_mensage(len(msg) ) ) # enviamos o tamanho da proxima mensagem que contera os dadso serealizados
        #print("enviando length")
        clientsocket.send( bytes(msg, 'utf-8')) # enviamos os dados serealizados
        #print("enviando dados")
    except:
        pass

def socket_sensor_delete(pacients,sokt):
    '''
    Função da thread para os sockets de DELETE

    @param pacientes: dicionario contendo o objeto que guarda os pacientes no sistema
    @param sokt: socket que essa thread estara responsavel por lida
    '''
    try:
        (clientsocket, address) = sokt.accept() # aceitamos a conecção
        msg = util.read_from_socket(clientsocket,length=1024) # lemos a mensagem
        del(pacients[msg["paciente"]]) # tentamos remover o paciente informado
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
    return cont