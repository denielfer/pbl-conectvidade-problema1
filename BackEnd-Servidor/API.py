import server_dinamic_socket
from flask import Flask,jsonify
import socket
from json import JSONDecoder
import util

app = Flask(__name__)

decoder = JSONDecoder()

def get_dados():
    '''
    Esta função tenta se conectar com o servirdo especificado nas constantes {IP} na porta {BASE_PORT} e retorna o conjunto de pacientes daquele sistema

    @return, dicionario, contendo o conjunto de pacientes do sistema

    @raise Exception se a conecção nao for aceita pelo server ou quebrada por qualquer motivo

    Esta função pode gerar erro de timeout caso o servidor demore mais de 60 para responder e de uma exception caso a conecção nao seja aceita.
    '''


@app.route('/', methods=['GET'])
def api_get():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#criamso o socket
    server_socket.connect((server_dinamic_socket.ip,server_dinamic_socket.port))#tentamos nos conectar com o servidor
    request = {'action':'GET'}#objeto que sera enviado
    server_socket.send( util.padding_mensage(request) )#enviamos a ação desejada
    resp = util.read_from_socket(server_socket) #lemos a resposta do servidor
    server_socket.close()#fechamos a conecção
    if(resp["statusCode"]):# se a conecção foi aceita
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as get_socket: #criamos um socket
            get_socket.settimeout(60)#caso ele fique esperando resposta ou tentando se sonectar por 60s criamos um erro
            get_socket.connect((server_dinamic_socket.ip,resp["data"]["port"]))#tentamos nos conectar ao servirdor
            length = int(get_socket.recv(util.INITIAL_PACKAGE_LENGTH)) #lemos a primeira mensagem que dira o tamanho da proxima contendo os dados dos pacientes
            msg_b = str(get_socket.recv(length),'utf-8')#lemos os dados dos pacientes
            server_socket.close()#fechamos a conecção
            return decoder.decode(msg_b),200 #retornamos os dados em um json com o codigo 200
            #print ('recebidos: \n', data)
    else:    #caso a conecção seja recusada
#        print("Conexão recusada")
        return {},404
    

app.run()