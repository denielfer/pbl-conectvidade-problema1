import socket
import json
from . import util

decoder = json.JSONDecoder()

ip = "26.181.221.42"
BASE_PORT = 12500

def get_dados():
    '''
    Esta função tenta se conectar com o servirdo especificado nas constantes {IP} na porta {BASE_PORT} e retorna o conjunto de pacientes daquele sistema

    @return, dicionario, contendo o conjunto de pacientes do sistema

    @raise Exception se a conecção nao for aceita pelo server ou quebrada por qualquer motivo

    Esta função pode gerar erro de timeout caso o servidor demore mais de 60 para responder e de uma exception caso a conecção nao seja aceita.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#criamso o socket
    server_socket.connect((ip,BASE_PORT))#tentamos nos conectar com o servidor
    request = {'action':'GET'}#objeto que sera enviado
    server_socket.send( util.padding_mensage(request) )#enviamos a ação desejada
    resp = util.read_from_socket(server_socket) #lemos a resposta do servidor
    server_socket.close()#fechamos a conecção
    if(resp["statusCode"]):# se a conecção foi aceita
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as get_socket: #criamos um socket
            get_socket.settimeout(60)#caso ele fique esperando resposta ou tentando se sonectar por 60s criamos um erro
            get_socket.connect((ip,resp["data"]["port"]))#tentamos nos conectar ao servirdor
            length = int(get_socket.recv(util.INITIAL_PACKAGE_LENGTH)) #lemos a primeira mensagem que dira o tamanho da proxima contendo os dados dos pacientes
            msg_b = str(get_socket.recv(length),'utf-8')#lemos os dados dos pacientes
            server_socket.close()#fechamos a conecção
            return decoder.decode(msg_b)#retornamos os dados em um dicionario
            #print ('recebidos: \n', data)
    else:    #caso a conecção seja recusada
#        print("Conexão recusada")
        raise("Conexão recusada")#geramos um erro