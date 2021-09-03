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

    Esta função pode gerar erro de timeout caso o servidor demore mais de 60 para responder e de uma exception caso a conecção nao seja aceita.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((ip,BASE_PORT))
    request = {'action':'GET'}
    server_socket.send( util.padding_mensage(request) )
    resp = util.read_from_socket(server_socket)
    if(resp["accepted"]):
        print("request aceito")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as get_socket:   
            get_socket.settimeout(60)
            get_socket.connect((ip,resp["port"]))
            print("conectado")
            length = int(get_socket.recv(util.INITIAL_PACKAGE_LENGTH))
            print("length recebido")
            msg_b = str(get_socket.recv(length),'utf-8')
            server_socket.close()
            return decoder.decode(msg_b)
            #print ('recebidos: \n', data)
    else:    
        server_socket.close()
        print("Conexão recusada")
        raise("Conexão recusada")