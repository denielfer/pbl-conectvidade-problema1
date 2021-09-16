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
    '''
    return server_dinamic_socket.pacientes,200 #retornamos os dados em um json com o codigo 200

app.run(host=f"{server_dinamic_socket.ip}", port=5000)