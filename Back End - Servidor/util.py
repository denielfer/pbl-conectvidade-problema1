import pickle

INITIAL_PACKAGE_LENGTH = 64

def read_from_socket(sokt,length=INITIAL_PACKAGE_LENGTH):
    '''
    Essa função retorna um dicionario que é construido com base no vetor de 
        bytes presente no buffer do {sokt}, pegando um tamanho {length}

    @param sokt, socket.socket que no qual a leitura sera realizada
    @param length, int informando o tamnho da mensagem que sera lida, por 
        default é INITIAL_PACKAGE_LENGTH

    Esta função tenta monta um dicionario usando pickle.loads com os dados no 
        buffer, cado os dados do buffer sejam b'', ou seja vazio, é retornado {},
        um dicionario vazio, caso contrario é tentado monta o dicionario apartir 
        dos dados lidos, o que pode gerar erro caso os dados enviados nao estejam
        na forma correta, erro este que nao é tratado nesta função
    '''
    msg_bytes = sokt.recv(length)
    #print(f"mensagem em bytes {msg_bytes}")
    if(msg_bytes == b''):
        return {}
    return pickle.loads(msg_bytes)

def padding_mensage(returned_msg,length=INITIAL_PACKAGE_LENGTH):
    '''
    Essa função da um padding na mensagem ate ela ter {length} de tamanho

    @param returned_msg é uma variavel que contem a mensagem na qual sera feita o 
        padding, esta variavel passara por um processo de processo de serealização 
        antes da adição do padding
    @param length, int, sendo o tamanho maximo da mensagem com padding
    @return, b-string, string binaria com a mensagem seriealizada e com padding adicionado

    Note que nesta função nao se verifica se o tamanho da mensagem é menor que o 
        padding, logo, nao se ten tratamento para esse caso
    '''
    msg = pickle.dumps(returned_msg)
    return msg+ (b''*(length-len(msg)))