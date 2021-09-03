from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .pacient_thread import Pacientes_threads
from . import util

IP = "26.181.221.42"
BASE_PORT = 12500
LENGTH_DO_IDENTIFICADOR = 10

#objeto onde sera mantido o dados internamente dos paciente no 
#   gerador para serem enviados para o servidor
pacientes = {} # consiste em um dicionario com a chave o identificador e nos dados é guardado um vetor dos dados do paciente seguindo a ordem {sequencia_dados}
#Qual os codigos dos dados no servidor que os dados terao
sequencia_dados=["preção", "oxigenação", "frequencia","temperatura"]
#Qual o type do campo no HTML que esse dado deve ter
TIPO_DOS_DADOS=['number',"number","number","number"] #"text"
TEMPO_DE_ENVIO_EM_SEGUNDOS = 5 # de quanto em quanto tempo os dados serao enviados

#inicia o objeto que é responsavel por maneja as threads de dispositivos
dispositivos = Pacientes_threads(IP,BASE_PORT, sequencia_dados, TEMPO_DE_ENVIO_EM_SEGUNDOS)

def go_home():
    return redirect("listar_pacientes")
    
def add_paciente(request):
    if(request.method == 'POST'):
        #Geramos um identificador aleatorio
        nome = util.get_random_string(LENGTH_DO_IDENTIFICADOR)
        while(nome in pacientes):
            #caso esse identificador ja esteja me uso geramos outro ate nao estar mais
            nome = util.get_random_string(LENGTH_DO_IDENTIFICADOR)
        pacientes[nome]=[0 if(a=="number") else "" for a in TIPO_DOS_DADOS] # iniciamos os dados do paciente como 'nulos', o para numero e string vazia para nao numeros
        dispositivos.add_paciente(nome,pacientes[nome]) #adicionamos o paciente no gestor de dispositivos
    return go_home() # redirecionamos o request para home page

def editar_paciente(request,nome):
    if(nome in pacientes and request.method == 'POST'):
        try:
            dados = [request.POST.get(a) for a in sequencia_dados]
            pacientes[nome]= dados
            dispositivos.remover_paciente(nome) #destruimos a thread antiga que tinha os dados erados
            dispositivos.add_paciente(nome,pacientes[nome])# e criamos uma thread nova com os dados corretos
        except:
            pass
    return go_home()

def remove_paciente(request,nome):
    if( nome in pacientes and request.method == 'POST'):
        try:
            dispositivos.remover_paciente(nome)
            del(pacientes[nome])
        except:
            print(f"nao foi poscivel deletar paciente com identificação: {nome} ")
    return go_home()

def get_pacient_data():
    pacientes_nomes = [a for a in pacientes]
    pacientes_dados = [ [(campo,dado,tipo) for campo,dado,tipo in zip(sequencia_dados, pacientes[a],TIPO_DOS_DADOS)] for a in pacientes]
    return { "campos":sequencia_dados,"pacientes_nome_dados":zip(pacientes_nomes,pacientes_dados), 'num_pacientes':len(pacientes)!=0 }

def pagina_de_pacientes(request):
    try:
        util.ping((IP,BASE_PORT))    
    except:
        template = loader.get_template("server_off.html")
        return HttpResponse(template.render({"tempo_espera":TEMPO_DE_ENVIO_EM_SEGUNDOS*1000},request))
    contexto = get_pacient_data()
    template = loader.get_template("pacientes.html")
    return HttpResponse(template.render(contexto,request))
