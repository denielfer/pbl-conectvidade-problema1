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
def thread_main_socket_heandler(ip:int,port:str,pacientes:dict) -> None:
    server_main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_main_socket.bind((ip, port)) #colocamoso  socket para ouvir no ip e porta informados
    server_main_socket.listen(4000) # quantidade de conecções na fila de espera
    while True: #estaremos sempre
        returned_msg = {"statusCode":404} # deixamos pre setado um retorno informand que a ação nao foi realizada
        thread = None
        #print(f'[SERVER] New Client: {adr}')
        try: 
            client_socket, adr = server_main_socket.accept() #aceitando conecções
            msg = util.read_from_socket(client_socket) # tentamos efetua a leitura de 128 bytes no buffer
            # entao a depender do que seja solicitado vamos criar uma thread com um determinado comportamento para lida com o pedido do cliente
            if(msg["action"] == "GET"):
                thread = threading.Thread(target=server_dinamic_actions.socket_get_action,  args=(pacientes,client_socket,adr))
            elif (msg["action"] == "POST" or msg["action"] == "PUT"): # em caso de POST ou PUT a ação é a mesma
                thread = threading.Thread(target=server_dinamic_actions.socket_sensor_action,  args=(pacientes,client_socket,msg['headers']))
            elif (msg["action"] == "DELETE"): #caso DELETE
                thread = threading.Thread(target=server_dinamic_actions.socket_sensor_delete,  args=(pacientes,client_socket,msg['headers']))
            if(thread != None):
                returned_msg["statusCode"] = 200 # definimos que o resultado do request foi resolvido com sucesso
        except Exception: # caso haja uma exception vamos printan o terminal que nao deu certo e a resposta nao chegou a ser alterada, entao nao precisa se tomar outra ação pois responderemos ao cliente com um 404
            #se der um erro printamos erro no terminal e returned_msg nao vai ter sido atualizada
            print(f"ALGUM ERRO ACONTECEU COM O REQUEST DE :{adr}")
        if(returned_msg["statusCode"] == 200): # se a requesição foi aceita com sucesso adicionamos os dados na resposta
            print(f"[SERVER] {adr} foi aceito para: {msg['action']}")
            thread.start()
        else:
            print(f"[SERVER] {adr} NÃO foi aceito")
        if(client_socket != None and adr != None):
            client_socket.sendto( util.padding_mensage(returned_msg,64),adr) # enviamos a resposta

if(__name__=="__main__"): # se esse arquivo é rodado como principal criamos uma thread que roda a função
    threading.Thread(target=thread_main_socket_heandler,args=(ip,port,pacientes)).start()
else:# se importado criamos uma thread com atributo daemon = True, para que essa thread nao impeça o programa de encerra caso as main threads encerrem. ( no python um programa é finalizado quando nao existem mais no-daemon threads sendo executadas)
    main_thread = threading.Thread(target=thread_main_socket_heandler,args=(ip,port,pacientes))
    main_thread.setDaemon(True)
    main_thread.start() 