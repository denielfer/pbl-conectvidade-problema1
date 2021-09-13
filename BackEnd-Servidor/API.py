import server_dinamic_socket
from flask import Flask,jsonify
import socket
from json import JSONDecoder
import util

app = Flask(__name__)

decoder = JSONDecoder()

@app.route('/', methods=['GET'])
def api_get():
    '''
        Função que retorna uma reposta json contendo os pacientes do sistema
        Ela faz um request atravez de sockets para o backend e então repassa para quem fez o request para essa API
    '''
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#criamso o socket
        server_socket.connect((server_dinamic_socket.ip,server_dinamic_socket.port))#tentamos nos conectar com o servidor
        request = {'action':'GET','headers':{}}#objeto que sera enviado
        server_socket.send( util.padding_mensage(request) )#enviamos a ação desejada
        resp = util.read_from_socket(server_socket,64) #lemos a resposta do servidor
        if(resp["statusCode"]):# se a conecção foi aceita
            length = int(server_socket.recv(128)) #lemos a primeira mensagem que dira o tamanho da proxima contendo os dados dos pacientes
            msg_b = str(server_socket.recv(length),'utf-8')#lemos os dados dos pacientes
            server_socket.close()#fechamos a conecção
            return decoder.decode(msg_b),200 #retornamos os dados em um json com o codigo 200
        else:    #caso a conecção seja recusada
            return {},404
    except:
        return {},404

app.run(host=f"{server_dinamic_socket.ip}", port=5000)