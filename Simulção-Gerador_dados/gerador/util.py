import json
import random
from string import ascii_lowercase
import socket

encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

INITIAL_PACKAGE_LENGTH = 64

def read_from_socket(sokt,length=INITIAL_PACKAGE_LENGTH):
    '''
    Essa função retorna um dicionario que é construido com base no vetor de 
        bytes presente no buffer do {sokt}, pegando um tamanho {length}

    @param sokt, socket.socket que no qual a leitura sera realizada
    @param length, int informando o tamnho da mensagem que sera lida, por 
        default é INITIAL_PACKAGE_LENGTH

    Esta função tenta monta um dicionario usando json.JSONEncoder.encode com os dados no 
        buffer, cado os dados do buffer sejam b'', ou seja vazio, é retornado {},
        um dicionario vazio, caso contrario é tentado monta o dicionario apartir 
        dos dados lidos, o que pode gerar erro caso os dados enviados nao estejam
        na forma correta, erro este que nao é tratado nesta função
    '''
    msg_bytes = str(sokt.recv(length),'utf-8')
    #print(f"mensagem em bytes {msg_bytes}")
    if(msg_bytes == b''):
        return {}
    return decoder.decode(msg_bytes)

def padding_mensage(returned_msg,length=INITIAL_PACKAGE_LENGTH):
    '''
    Essa função da um padding na mensagem ate ela ter {length} de tamanho

    @param returned_msg é uma variavel que 
    @return b-string com {returned_msg} encoded e com o padding
    '''
    msg = encoder.encode(returned_msg)
    msg = bytes(msg, 'utf-8')
    return msg+ (b' '*(length-len(msg)))

def get_random_string(length:int):
    '''
    Gera uma string de caracteris minusculos aleatorias com o tamanho 
        informado {length}
    
    @param length, int, tamanho da string a ser gerada
    '''
    return ''.join(random.choices(ascii_lowercase, k = length))


def ping(adr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(adr)
    print(encoder.encode({"action":"ping"}))
    s.send(bytes(encoder.encode({"action":"ping"}),'utf-8'))
    s.close()