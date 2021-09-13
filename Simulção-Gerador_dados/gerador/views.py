from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .pacient_thread import Pacientes_threads
from . import util

IP = "26.181.221.42" #ip da maquina que esta rodando o servidor (backend)
BASE_PORT = 12500 #porta base para o serviço do servidor (backend)

LENGTH_DO_IDENTIFICADOR = 10
#objeto onde sera mantido o dados internamente dos paciente no 
#   gerador para serem enviados para o servidor
pacientes = {} # consiste em um dicionario com a chave o identificador e nos dados é guardado um vetor dos dados do paciente seguindo a ordem {sequencia_dados}
#Qual os codigos dos dados no servidor que os dados terao
sequencia_dados=["pressão", "oxigenação", "frequencia","temperatura"]
#Qual o type do campo no HTML que esse dado deve ter
TIPO_DOS_DADOS=['number',"number","number","number"] #"text"
TEMPO_DE_ENVIO_EM_SEGUNDOS = 5 # de quanto em quanto tempo os dados serao enviados

#inicia o objeto que é responsavel por maneja as threads de dispositivos
dispositivos = Pacientes_threads(IP,BASE_PORT, sequencia_dados, TEMPO_DE_ENVIO_EM_SEGUNDOS)

# for a in range(100):
#     nome = a # gera um identificador aleatorio para o dispostivo
#     while(nome in pacientes): # se o nome em uso gera outro ate achar um valido
#         #caso esse identificador ja esteja me uso geramos outro ate nao estar mais
#         nome = util.get_random_string(LENGTH_DO_IDENTIFICADOR)
#     pacientes[nome]=[0 if(a=="number") else "" for a in TIPO_DOS_DADOS] # iniciamos os dados do dispositivo como 'nulos', o para numero e string vazia para nao numeros
#     dispositivos.add_paciente(nome,pacientes[nome]) #adicionamos o dispostivo no gestor de dispositivos

def go_home():
    '''
        Função que faz um redirect para a pagina inicial ( isso é usado para redireciona requestes para outros rotas para a pagina inicial )
    '''
    return redirect("listar_pacientes")
    
def add_paciente(request):
    '''
    função chamada pela url de adição de paciente
    '''
    if(request.method == 'POST'):# se metodo post
        #Geramos um identificador aleatorio
        nome = util.get_random_string(LENGTH_DO_IDENTIFICADOR) # gera um identificador aleatorio para o dispostivo
        while(nome in pacientes): # se o nome em uso gera outro ate achar um valido
            #caso esse identificador ja esteja me uso geramos outro ate nao estar mais
            nome = util.get_random_string(LENGTH_DO_IDENTIFICADOR)
        pacientes[nome]=[0 if(a=="number") else "" for a in TIPO_DOS_DADOS] # iniciamos os dados do dispositivo como 'nulos', o para numero e string vazia para nao numeros
        print("dfc0")
        dispositivos.add_paciente(nome,pacientes[nome]) #adicionamos o dispostivo no gestor de dispositivos
    return go_home() # redirecionamos o request para home page

def editar_paciente(request,nome):
    '''
    Função que lida com a edição do paciente
 
    @param nome corresponde ao codigo de identificação do dispositivo do paciente no sistema
    '''
    if(nome in pacientes and request.method == 'POST'):# se post
        try:
            dados = [request.POST.get(a) if(TIPO_DOS_DADOS[n] != "number") else float(request.POST.get(a)) for n,a in enumerate(sequencia_dados)] # tentamos recupera todos so dados nos seus ticos corretos
            pacientes[nome]= dados# alteramos os dados na memoria do sistema
            #entao mechemos na threads que fica enviando os dados periodicamente
            dispositivos.remover_paciente(nome) #destruimos a thread antiga que tinha os dados erados
            dispositivos.add_paciente(nome,pacientes[nome])# e criamos uma thread nova com os dados corretos
        except:
            pass
    return go_home()# redirecionamos para home page

def remove_paciente(request,nome):
    '''
    função que lida com a remoção de paciente

    @param nome corresponde ao codigo de identificação do dispositivo do paciente no sistema
    '''
    if( nome in pacientes and request.method == 'POST'):# se POST
        try:
            dispositivos.remover_paciente(nome) #removemos o dispositivo
            del(pacientes[nome])# deletamos do sistema
        except:# caso de erro é pois ele nao esta no sistema, simplismente colocamos qual o codigo erdo no terminal
            print(f"nao foi poscivel deletar paciente com identificação: {nome} ")
    return go_home()#redirecionamos para home page

def get_pacient_data():
    '''
    Função que retorna os dados dos paciente no sistema, usada internamente para monta home page
    '''
    pacientes_nomes = [a for a in pacientes]#salvamos os domes do paciente, identificador dos dispositvos
    pacientes_dados = [ [(campo,dado,tipo) for campo,dado,tipo in zip(sequencia_dados, pacientes[a],TIPO_DOS_DADOS)] for a in pacientes]# salvamos os dados dos sensores
    return { "campos":sequencia_dados,"pacientes_nome_dados":zip(pacientes_nomes,pacientes_dados), 'num_pacientes':len(pacientes)!=0 } # retornamos um dicionario contendo os dados nescessarios para renderizar o html da home page

def pagina_de_pacientes(request):
    '''
    função que gera a home page
    '''
    try:
        util.ping((IP,BASE_PORT)) #verificamos se o servidor, servidor do projeto que se comunica com a interfacie do medico, esta online
    except:
        template = loader.get_template("server_off.html")# caso der erro renderizamos um hmtl padrao de erro
        return HttpResponse(template.render({"tempo_espera":TEMPO_DE_ENVIO_EM_SEGUNDOS*1000},request)) # aqui é feita a montagem do html
    contexto = get_pacient_data() # pegamos os dados nescessarios para monta o html da home page
    template = loader.get_template("pacientes.html") # caregamos o template html
    return HttpResponse(template.render(contexto,request)) #montamos os html que sera retornado
