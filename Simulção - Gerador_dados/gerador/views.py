from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .pacient_thread import pacientes_threads

pacientes = {}
sequencia_dados=["preção", "frequencia respiratoria", "oxigenação no sangue"]
tipo_de_dado=['number',"number","number"] #"text"

threads = pacientes_threads("http://127.0.0.1:8000",sequencia_dados,1)

import random
from string import ascii_lowercase

def go_home():
    return redirect("listar_pacientes")
    
def add_paciente(request):
    if(request.method == 'POST'):
        nome = ''.join(random.choices(ascii_lowercase, k = 5))
        while(nome in pacientes):
            nome = ''.join(random.choices(ascii_lowercase, k = 5))
        pacientes[nome]=[0 if(a=="number") else random.choices(ascii_lowercase, k = 5) for a in tipo_de_dado]
        threads.add_paciente(nome,pacientes[nome])
    return go_home()

def editar_paciente(request,nome):
    if(nome in pacientes and request.method == 'POST'):
        dados = [request.POST.get(a) for a in sequencia_dados]
        pacientes[nome]= dados
        threads.remover_paciente(nome)
        threads.add_paciente(nome,pacientes[nome])
    return go_home()

def remove_paciente(request,nome):
    if( nome in pacientes and request.method == 'POST'):
        del(pacientes[nome])
        threads.remover_paciente(nome)
    return go_home()

def get_pacient_data():
    pacientes_nomes = [a for a in pacientes]
    pacientes_dados = [ [(campo,dado,tipo) for campo,dado,tipo in zip(sequencia_dados, pacientes[a],tipo_de_dado)] for a in pacientes]
    return { "campos":sequencia_dados,"pacientes_nome_dados":zip(pacientes_nomes,pacientes_dados), 'num_pacientes':len(pacientes)!=0 }

def pagina_de_pacientes(request):
    contexto = get_pacient_data()
    template = loader.get_template("pacientes.html")
    return HttpResponse(template.render(contexto,request))
