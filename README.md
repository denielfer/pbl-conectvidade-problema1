# Descrição #
 Este repositorio comtem os arquivos criados para resolução do 1º problema da materia TEC502 - MI - CONCORRÊNCIA E CONECTIVIDADE, que pode ser visto [aqui](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/Apresenta%C3%A7%C3%A3o_do_Problema.pdf)
 Neste repositorio temos 3 sistemas:
  - BackEnd-Servidor: corresponde ao sistema que representa o servidor no qual os dados serao mantidos e é responsavel por redistribuilos conforme solicitado
  - FrontEnd-Monitor: Corresponde ao sistema que mostrara os dados para o medico, a comunicação entre este e o back pode ser feito atravez de sockets ou por requests
  - Simulção-Gerador_dados: Corresponde ao sistema que emula os dispostivos e envia os dados para o servidor
# Instalação #
1 - Instala [python](https://www.python.org/)
  
2 - Crie um ambiente virtual e inicie ele.[Mais informações](https://docs.python.org/3/library/venv.html)
  
      python3 -m venv /path/to/new/virtual/environment
      /path/to/new/virtual/environment\Scripts\activate

    
3 - Instale os requesitos nescessarios no requirements.txt
  
      pip install -r requirements.txt
    
4 - inicia sistemas

 Estes passos não precisam ser feitos na ordem aqui especificada
   
4.1 - inicia BackEnd-Servidor:
    
 Em um terminal inicio o sistema com:
      
    python3 .\BackEnd-Servidor\API.py

4.2 - inicia Simulção-Gerador_dados:
 Em um terminal inicio o sistema com:
    
    python3 .\Simulção-Gerador_dados\manage.py runserver __my_ip__:__porta__
   
      
4.3 - inicia FrontEnd-Monitor:
    
 Em um terminal inicio o sistema com:
      
    
    python3 .\FrontEnd-Monitor\manage.py runserver __my_ip__:__porta__
    
Recomendações: caso os sistemas não estejam em uma rede local pode se usar [Radmin VPN](https://www.radmin-vpn.com/br/), para windowns, ou abri pode abri as portas do roteador para que ele funcione na rede, a porta na qual a api esta usando no servidor, e assim o FrontEnd teria que conseguir os dados pelo request, no sistema do Frontend e no sistema de Simulção a porta na qual foi inicializada o sistema na linha do terminal, porem ainda assim seria nescessario que a maquina com o sistema de Simulção deve esta na mesma rede local que o BackEnd, pois a comunicação dos mesmos é feito atravez de sockets, para mais detalhes tem: [Diagramas de Fluxo](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/Diagrama%20de%20fluxo.png) e [Diagrama de Sequencia](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/diagrama%20de%20sequencia.png).
  
#Manuais:
 - [Manual de usuario - Medico](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/Manual%20de%20usuario%20-%20Medico.md)
 - [Manual de Usuario - Gerador de dados](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/Manual%20de%20Usuario%20-%20Gerador%20de%20dados.md)
 - [Manual de Sistema](https://github.com/denielfer/pbl-conectvidade-problema1/blob/main/Manual%20de%20Sistema.md)
