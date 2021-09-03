import socket
import server_actions
from time import sleep
import util
import threading

pacientes= {}
NUM_SOCKETS_POST_PUT = 10
NUM_SOCKETS_GET = 2
NUM_SOCKETS_DELETE = 5
QUEUE_BASE_SIZE = 100

#COnfigurando o socket de etnrada
server_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "0.0.0.0"
port = 12500
server_main_socket.bind((ip, port))
server_main_socket.listen(4*QUEUE_BASE_SIZE)
#configurando os sockets de GET requests
server_get_sockets = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(NUM_SOCKETS_GET) ]
for a,sokt in enumerate(server_get_sockets):
    sokt.bind((ip,port-a-1))
    sokt.listen(3*QUEUE_BASE_SIZE)
    threading.Thread(target=server_actions.socket_get_action,  args=(pacientes,sokt)).start()
#    server_actions.server_socket_get_start(pacientes,sokt)

#configurando os sokets de POST e PUT requests
server_post_sockets = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(NUM_SOCKETS_POST_PUT) ]
for a,sokt in enumerate(server_post_sockets):
    sokt.bind((ip,port+a+1))
    sokt.listen(QUEUE_BASE_SIZE)
    threading.Thread(target=server_actions.socket_sensor_action,  args=(pacientes,sokt)).start()
#    server_actions.server_socket_sensor_start(pacientes,sokt)

#configurando os sockets de DELETE requests
server_delete_sockets = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(NUM_SOCKETS_DELETE) ]
for a,sokt in enumerate(server_delete_sockets):
    sokt.bind((ip,port+NUM_SOCKETS_POST_PUT+a+1))
    sokt.listen(QUEUE_BASE_SIZE)
    threading.Thread(target=server_actions.socket_sensor_delete,  args=(pacientes,sokt)).start()
#    server_actions.server_socket_delete_start(pacientes,sokt)

post_socket_index = 1
get_socket_index = 1
delet_socket_index = 1
while True:
    client_socket, adr = server_main_socket.accept()
    returned_msg = {"accepted":False}
    #print(f'[SERVER] New Client: {adr}')
    try:
        msg = util.read_from_socket(client_socket)
        # print(msg)
        if(msg["action"] == "GET"):
            #caso nao tenha o campo "action" isso gerara um erro o que acarreta no 
            #  envio da mensagem informando que a coneção nao foi aceita
            # se nao ocorrer o erro definimos com qual soquet esse request de GET
            #  deve se comunicar daqui para frente
            returned_msg["port"] = port-get_socket_index
            get_socket_index+=1
            if(get_socket_index == NUM_SOCKETS_GET+1):
                get_socket_index=1 
            returned_msg["accepted"] = True
        elif (msg["action"] == "POST" or msg["action"] == "PUT"):	
        #caso a ação seja de PUT or POST aqui achamos um soket pra ele se comunicar
            returned_msg["port"] = port+post_socket_index
            post_socket_index+=1
            if(post_socket_index == NUM_SOCKETS_POST_PUT+1):
                post_socket_index=1
            returned_msg["accepted"] = True
        elif (msg["action"] == "DELETE"):	
        #caso a ação seja DELETE define o socket que ele deve se comunicar
            returned_msg["port"] = port+NUM_SOCKETS_POST_PUT+delet_socket_index+1
            delet_socket_index+=1
            if(delet_socket_index == NUM_SOCKETS_DELETE+1):
                delet_socket_index=1
            returned_msg["accepted"] = True
    except Exception:
        #se der um erro printamos erro no terminal e returned_msg nao vai ter sido atualizada
        print(f"ALGUM ERRO ACONTECEU COM O REQUEST DE :{adr}")
    if(returned_msg["accepted"]): 
        print(f"[SERVER] {adr} foi aceito para: {msg['action']} -> {returned_msg['port']}")
    else:
        print(f"[SERVER] {adr} NÃO foi aceito")
    client_socket.sendto( util.padding_mensage(returned_msg),adr)
    sleep(.001)
    client_socket.close()
