import socket
import server_dinamic_actions
from time import sleep
import util
import threading

#onde guardaremos os dados
pacientes= {}

#COnfigurando o socket de etnrada
ip = "26.181.221.42" #ip onde que o socket estara ouvindo
port = 12500     #porta que o socket estara ouvindo
def thread_main_socket_heandler(ip,port,pacientes):
    server_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_main_socket.bind((ip, port)) #colocamoso  socket para ouvir no ip e porta informados
    server_main_socket.listen(40000) # quantidade de conecções na fila de espera
    while True: #estaremos sempre
        returned_msg = {"statusCode":404} # deixamos pre setado um retorno informand que a ação nao foi realizada
        data = {}
        #print(f'[SERVER] New Client: {adr}')
        try: 
            client_socket, adr = server_main_socket.accept() #aceitando conecções
            msg = util.read_from_socket(client_socket) # tentamos efetua a leitura de 128 bytes no buffer
            sokt = None # criamos a variavel que tera o socket para a conecção com o cliente
            while(sokt==None): # enquanto nao houver um socket para o cliente
                try: # tentaremos criar um socket
                    port+=1 # sempre tentando na proxima porta
                    sokt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criamos um socket
                    sokt.bind((ip,port)) #tentamos colocalo no {ip} e na porta que estamos testando
                    sokt.listen(1) # se nao houve problema na criação, quantidade de conecções que ele ira deixa esperando é 1, pois ele deve responder apenas a 1 request
                    data["port"] = port # colocamos na mensagem que sera enviada de volta qual a porta ele deve se dirigir
                except: # se ocorrer alguma exception no processo a acima seria por problema na criação do socket
                    sokt = None # entao tiramos o abjeto que poderia ter sido criado acima
                    data["port"] = None 
                if(port>60000): # caso chegemos nessa porta iremos volta a procura do inicio
                    port=12500
            # print(msg)
            # entao a depender do que seja solicitado vamos criar uma thread com um determinado comportamento para lida com o pedido do cliente
            if(msg["action"] == "GET"): # caso o pedido seja de GET
                #caso nao tenha o campo "action" isso gerara um erro o que acarreta no 
                #  envio da mensagem informando que a coneção nao foi aceita pois cairia na except abaixo
                # se nao ocorrer o erro criamos a thread que lidara com o cliente
                threading.Thread(target=server_dinamic_actions.socket_get_action,  args=(pacientes,sokt)).start()
            elif (msg["action"] == "POST" or msg["action"] == "PUT"): # em caso de POST ou PUT a ação é a mesma
                threading.Thread(target=server_dinamic_actions.socket_sensor_action,  args=(pacientes,sokt)).start()
            elif (msg["action"] == "DELETE"): #caso DELETE
                threading.Thread(target=server_dinamic_actions.socket_sensor_delete,  args=(pacientes,sokt)).start()
            returned_msg["statusCode"] = 200 # definimos que o resultado do request foi resolvido com sucesso
        except Exception: # caso haja uma exception vamos printan o terminal que nao deu certo e a resposta nao chegou a ser alterada, entao nao precisa se tomar outra ação pois responderemos ao cliente com um 404
            #se der um erro printamos erro no terminal e returned_msg nao vai ter sido atualizada
            print(f"ALGUM ERRO ACONTECEU COM O REQUEST DE :{adr}")
        if(returned_msg["statusCode"] == 200): # se a requesição foi aceita com sucesso adicionamos os dados na resposta
            returned_msg["data"] = data
            print(f"[SERVER] {adr} foi aceito para: {msg['action']} -> {data['port']}")
        else:
            print(f"[SERVER] {adr} NÃO foi aceito")
        if(client_socket != None and adr != None):
            client_socket.sendto( util.padding_mensage(returned_msg),adr) # enviamos a resposta

def get_dados():
    return pacientes
if(__name__=="__main__"):
    threading.Thread(target=thread_main_socket_heandler,args=(ip,port,pacientes)).start()
else:
    thread = threading.Thread(target=thread_main_socket_heandler,args=(ip,port,pacientes))
    thread.setDaemon(True)
    thread.start() 