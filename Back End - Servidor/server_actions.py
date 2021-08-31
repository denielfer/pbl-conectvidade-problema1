import threading
import pickle
import util
from time import sleep

def server_socket_sensor_start(pacientes,sokt):
    threading.Thread(target=socket_sensor_action,  args=(pacientes,sokt)).start()

def socket_sensor_action(pacients,sokt):
    # A PRIMIERA MENSAGEM DEVE CONTER {"lenght":length_da_proxima_mensagem} 
    # o que por padrao deixa com 512-27=485 bytes para o inteiro representando
    # {length_da_proxima_mensagem}
    while True:
        (clientsocket, address) = sokt.accept()
        msg = util.read_from_socket(clientsocket,length=1024)
        #print(f'atualizando: {msg["paciente"]}, dados: {msg["dados"]}')
        pacients[msg["paciente"]] = msg["dados"]
        sleep(.001)

def server_socket_get_start(pacientes,sokt):
    threading.Thread(target=socket_get_action, args=(pacientes,sokt)).start()

def socket_get_action(pacientes,sokt):
    while True:
        (clientsocket, address) = sokt.accept()
        msg = pickle.dumps(pacientes)
        clientsocket.send( util.padding_mensage(len(msg)) )
        clientsocket.send(msg)
        sleep(.001)

def server_socket_delete_start(pacientes,sokt):
    threading.Thread(target=socket_sensor_delete,  args=(pacientes,sokt)).start()

def socket_sensor_delete(pacients,sokt):
    # A PRIMIERA MENSAGEM DEVE CONTER {"lenght":length_da_proxima_mensagem} 
    # o que por padrao deixa com 512-27=485 bytes para o inteiro representando
    # {length_da_proxima_mensagem}
    while True:
        try:
            (clientsocket, address) = sokt.accept()
            msg = util.read_from_socket(clientsocket,length=1024)
            del(pacients[msg["paciente"]])
        except:
            pass