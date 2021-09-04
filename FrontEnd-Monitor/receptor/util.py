import json

encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

INITIAL_PACKAGE_LENGTH = 128

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
    msg_bytes = str(sokt.recv(length),'utf-8') #tenta ler o buffer do socket com o tamnho especificado
    #print(f"mensagem em bytes {msg_bytes}")
    if(msg_bytes == b''):#caso o buffer esteja vazio retorna um dicionario vazio
        return {}
    return decoder.decode(msg_bytes)#retorna os dados do buffer decodificados

def padding_mensage(returned_msg,length=INITIAL_PACKAGE_LENGTH):
    '''
    Essa função da um padding na mensagem ate ela ter {length} de tamanho

    @param returned_msg é uma variavel que 
    @return b-string com {returned_msg} encoded e com o padding
    '''
    msg = encoder.encode(returned_msg)#serealiza a os dados
    msg = bytes(msg, 'utf-8')#transforma em uma string binaria
    return msg+ (b' '*(length-len(msg)))#retorna a string binaria com um padding ( adicionando b" " na string ate chegar ao tamanho informado)


def check_if_prioridade(dados_do_paciente):
    '''
    Verifica se o paciente esta em estado critico com base nos dados

    @param dados_do_pacient, dicionario, com os dados do pacientes
    @return int sendo a prioridade do paciente

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