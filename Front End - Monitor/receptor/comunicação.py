import socket
import pickle
import util

ip = ""
BASE_PORT = 12500

def get_dados():
    '''
    Esta função tenta se conectar com o servirdo especificado nas constantes {IP} na porta {BASE_PORT} e retorna o conjunto de pacientes daquele sistema

    @return, dicionario, contendo o conjunto de pacientes do sistema

    Esta função pode gerar erro de timeout caso o servidor demore mais de 60 para responder e de uma exception caso a conecção nao seja aceita.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.timeout(60)
        server_socket.connect((ip,BASE_PORT))
        request = {'action':'GET'}
        server_socket.send( util.padding_mensage(request) )
        resp = util.read_from_socket(server_socket)
        if(resp["accepted"]):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as get_socket:   
                get_socket.settimeout(60)
                get_socket.connect((ip,resp["port"]))
                length = util.read_from_socket(get_socket)
                msg_b = get_socket.recv(length)
                return pickle.loads(msg_b)
                print ('recebidos: \n', data)
        else:
            print("Conexão recusada")
            raise("Conexão recusada")