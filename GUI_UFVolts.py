'''
\\\\\\UFVOLTS MAJORADOS////////

Acompanhamento dos dados em tempo real do protótipo FSAE recebidos via rádio, coletados pelo módulo HC-12
Simulação realizada com o auxílio dos softwares:
-Virtual Serial Ports Emulator
-Proteus (esquemática de circuito com código para o PIC)

Autores iniciais: Déric Augusto, Gustavo Giacomin, Mayelli Costa e Sandro Manoel.   

'''

# NOTE: Esse programa está configurado para a leitura do pacote de dados indicado à baixo e Baud Rate de 9600.
'''
String recebida pelo HC-12 (ou pela simulação): -VVVAPPTMTIBBP1P2BHV
      onde: 
              1. "-" é o handshake usado
              2. O número de letras é correspondente ao número de bytes enviados,
                 ou seja, 19 bytes no total e que VVV = 3 bytes, P1 = 2 bytes, etc..
              3. E é correspondente:
                                     VVV = VELOCIDADE
                                     APP = SINAL DO APPS
                                     TMT = TEMPERATURA DO MOTOR
                                     IBB = IMD, BMS, BSPD
                                     P1 = PRESSÃO FREIOS 1
                                     P2 = PRESSÃO FREIOS 2
                                     BHV = CARGA BATERIA HV

'''

#==================================================

import Botões as bt
import Gerador_de_Dados as gd
import Coleta_Dados_Serial as cds
import os # usada para: encerrar o programa e pegar o caminho do arquivo deste programa no sistema operacional
import threading # usada para execução de atividades de forma paralela
from datetime import datetime # usada para pegar o dado de tempo atual do computador
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation # a matplotlib é responsável por plotar gráficos
import matplotlib.animation as animation
matplotlib.use('TkAgg') # matplotlib no tkinter

# Tela do módulo TkAgg onde serão plotados os graficos e a NavigationTollbar do matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import tkinter as tk
from tkinter import *

#Variáveis globais: -------------------------------------------------

# String que define o .txt onde serão armazenados os dados
#path = os.path.dirname(os.path.abspath(__file__))
#diretorio = '%s\\Dados da telemetria.txt' % path

# Flag do while da função coleta_de_dados:
#flag = 0

# Variáveis que armazenam os dados recebidos:
#VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = RTD = 0

# Variáveis de objetos:
canvas = 0
subplot1 = subplot2 = 0
#area_graficos = area_mostradores = legenda = graf_select = janela_config = status = 0

# Definindo dimensões do gráfico (eixos)
x_eixo = []
y_VEL = []
y_TM = []
y_PRESS1 = []
y_PRESS2 = []
y_APPS = []
y_HV = []

#Funções: -----------------------------------------------------------

def user_interface():
    global subplot1, subplot2, canvas#, status, area_graficos, area_mostradores, janela_config, legenda

    # Define a janela principal (objeto) da aplicação
    Interface = Tk()  

    # Definindo características da janela
    Interface.title('Telemetria UFVolts Majorados')
    Interface.state('zoomed')  # define que a janela fique em tela cheia
    Interface.iconbitmap('images/icon.ico')
    Interface['bg'] = "black" #'#%02x%02x%02x' %(200, 34, 34) # definindo a cor de fundo da janela (bg = background)

    # Criando frames
    bt.lateral_bar = LabelFrame(Interface, bg='#%02x%02x%02x' %(200, 34, 34), borderwidth=0, padx=10, pady=10)
    bt.lateral_bar.pack(side=LEFT, fill="y")

    bt.area_graficos = LabelFrame(Interface, bg="black", borderwidth=0, padx=20, pady=10)
    bt.area_graficos.pack(side=TOP, fill="both", expand=1)

    bt.area_mostradores = LabelFrame(Interface, bg="black", borderwidth=1, padx=20, pady=10)
    bt.area_mostradores.pack(side=BOTTOM, fill="x")

    # Inserindo imagens
    imagem_logo = PhotoImage(file="images/logoformula1.png") # importando imagem
    logoformula = Label(bt.area_mostradores, image=imagem_logo, borderwidth=0) #label com imagem
    logoformula.grid(row=1, column=1, sticky=S)

    imagem_legenda = PhotoImage(file="images/legenda.png") # importando imagem
    bt.legenda = Label(Interface, image=imagem_legenda, bg="black", borderwidth=0, padx=20, pady=10) #label com imagem

    # Criando botões
    bt.Botoes()

    # Adicionando labels
    status = Label(bt.area_mostradores, text="Status: sem conexão", fg="red", font='CenturyGothic 10 bold', bg='Black')
    status.grid(row=0, column=1, sticky=N)

    # Criando Canvas
    canvas = tk.Canvas(bt.area_mostradores, width=1500, height=300, highlightthickness=1, bg="black")
    canvas.grid(row=0, column=0, rowspan=2)

    # ADICIONANDO GRÁFICOS ----------------------------------------------------

    # Criando figura que será printada na interface do tkinter
    graficos = Figure(figsize=(20,9), dpi=75, facecolor="white")
    subplot1 = graficos.add_subplot(2,1,1)
    subplot2 = graficos.add_subplot(2,1,2)

    #  Criando funções de altura
    alt_press1 = 175 - 1.5*int(gd.PRESS1)
    alt_press2 = 175 - 1.5*int(gd.PRESS2)
    alt_BHV = 175 - 1.5*int(gd.HV)
    alt_temp = 175 - 1.5*int(gd.TM)
    alt_APPS = 50 + int(gd.APPS)

    #  Adicionando barras gráficas e LEDS de estado
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    tk.Canvas.create_circle = _create_circle
    
    if gd.IMD == "1":
        canvas.create_circle(1400, 35, 30, fill="green", outline="#DDD")
    else:
        canvas.create_circle(1400, 35, 30, fill="red", outline="#DDD")
    if gd.BMS == "1":        
        canvas.create_circle(1400, 105, 30, fill="green", outline="#DDD")
    else:        
        canvas.create_circle(1400, 105, 30, fill="red", outline="#DDD")
    if gd.BSPD == "1":        
        canvas.create_circle(1400, 175, 30, fill="green", outline="#DDD")
    else:        
        canvas.create_circle(1400, 175, 30, fill="red", outline="#DDD")
    if gd.RTD == "1":        
        canvas.create_circle(1400, 245, 30, fill="green", outline="#DDD")
    else:        
        canvas.create_circle(1400, 245, 30, fill="red", outline="#DDD")   

    canvas.create_text(1400,35, text = "IMD", fill = "black")
    canvas.create_text(1400,105, text = "BMS", fill = "black")
    canvas.create_text(1400,175, text = "BSPD", fill = "black")
    canvas.create_text(1400,245, text = "RTD", fill = "black")

    #LED de luz de freio
    canvas.create_circle(250, 50, 25, fill="red", outline="#DDD")
    canvas.create_text(250,50, text = "BREAK", fill = "white")

    #Barras de pressão
    canvas.create_rectangle(350,25,380,175,fill = "black", outline = "#DDD")
    canvas.create_rectangle(380,25,410,175,fill = "black", outline = "#DDD")
    canvas.create_rectangle(350,alt_press1,380,175,fill = "red",outline = "#DDD", tag='PRESS1')
    canvas.create_rectangle(380,alt_press2,410,175,fill = "red",outline = "#DDD", tag='PRESS2')
    canvas.create_text(365,15, text = "D", fill = "white")
    canvas.create_text(395,15, text = "T", fill = "white")
    canvas.create_text(435,25, text = "100 BAR", fill = "white")
    canvas.create_text(430,175, text = "0 BAR", fill = "white")

    #Barra da APPS
    canvas.create_rectangle(50,90,150,110,fill = "black", outline = "#DDD")
    canvas.create_rectangle(50,90,alt_APPS,110,fill = "green", outline = "#DDD", tag='APPS')    
    canvas.create_text(100,80, text = "APPS", fill = "white")
    canvas.create_text(50,80, text = "0%", fill = "white")
    canvas.create_text(150,80, text = "100%", fill = "white")

    #Bateria HV
    canvas.create_rectangle(510,25,540,175,fill = "black", outline = "#DDD")
    canvas.create_rectangle(510,alt_BHV,540,175,fill = "red",outline = "#DDD", tag='BHV')
    canvas.create_text(525,15, text = "HV", fill = "white")
    canvas.create_text(555,25, text = "100%", fill = "white")
    canvas.create_text(550,175, text = "0%", fill = "white")

    #Temperatura do motor
    canvas.create_rectangle(620,25,650,175,fill = "black", outline = "#DDD")
    canvas.create_rectangle(620,alt_temp,650,175,fill = "red",outline = "#DDD", tag='TEMP')
    canvas.create_text(635,15, text = "MOTOR", fill = "white")
    canvas.create_text(665,175, text = "0 °C", fill = "white")
    canvas.create_text(670,25, text = "100°C", fill = "white")


    # JANELA DE CONFIGURAÇÃO --------------------------------------------------------   
    bt.janela_config = LabelFrame(Interface)
    
    lb_cor_de_fundo = Label(bt.janela_config, text= 'Cor de Fundo')
    lb_cor_de_fundo.place(x=10, y= 20)

    cor_de_fundo = StringVar()
    cor_de_fundo.set('Preto')

    popupCor = OptionMenu(bt.janela_config, cor_de_fundo, 'Amarelo', 'Branco', 'Vermelho', 'Preto' )
    popupCor.place(x = 95, y = 20)

    def opcao_cor():
        cor = cor_de_fundo.get()
        if cor == 'Amarelo':
            Interface.configure(bg = 'yellow')
            bt.area_graficos.configure(bg = 'yellow')
            bt.area_mostradores.configure(bg = 'yellow')
            canvas.configure(bg = 'yellow')
        if cor == 'Branco':
            Interface.configure(bg = 'white')
            bt.area_graficos.configure(bg = 'white')
            bt.area_mostradores.configure(bg = 'white')
            canvas.configure(bg = 'white')
        if cor == 'Vermelho':
            Interface.configure(bg = '#%02x%02x%02x' %(200, 34, 34))
            bt.area_graficos.configure(bg = '#%02x%02x%02x' %(200, 34, 34))
            bt.area_mostradores.configure(bg = '#%02x%02x%02x' %(200, 34, 34))
            canvas.configure(bg = '#%02x%02x%02x' %(200, 34, 34))
        if cor == 'Preto':
            Interface.configure(bg = 'black')
            bt.area_graficos.configure(bg = 'black')
            bt.area_mostradores.configure(bg = 'black')
            canvas.configure(bg = 'black')
        #janela_config.destroy()

    bt_aplicar = Button(bt.janela_config, text = 'Aplicar', bd = 2, bg = 'white', fg = 'black', 
                        font = ('verdana', 8), command = opcao_cor)           
    bt_aplicar.place(x = 40, y = 100)


    # Função que anima o gráfico
    def animate(i):
        global subplot1, subplot2#, graf_select, VEL, TM, PRESS1, PRESS2, 

        #Tempo real para gráfico
        data_hora_atual = datetime.now()
        minuto_segundo_milisegundo = data_hora_atual.strftime('%M:%S.%f')[:-3]

        # Atualizando valores
        x_eixo.append(minuto_segundo_milisegundo)
        y_VEL.append(gd.VEL)
        y_TM.append(gd.TM)
        y_PRESS1.append(gd.PRESS1)
        y_PRESS2.append(gd.PRESS2)

        if len(x_eixo) > 16:
            aux = x_eixo.pop(0)
            aux = y_VEL.pop(0)
            aux = y_TM.pop(0)
            aux = y_PRESS1.pop(0)
            aux = y_PRESS2.pop(0)

        # clear axes (limpa o gráfico entre um frame e outro)
        subplot1.cla()
        subplot2.cla() 

        # Plotando variáveis no gráfico
        if bt.graf_select == 0:
            subplot1.plot(x_eixo, y_VEL, label='Velocidade')
        if bt.graf_select == 1:
            subplot1.plot(x_eixo, y_TM, label='Temperatura')
        subplot1.legend(loc='upper left')

        subplot2.plot(x_eixo, y_PRESS1, label='Pressão D')
        subplot2.plot(x_eixo, y_PRESS2, label='Pressão T')
        subplot2.legend(loc='upper left') 


        # Atualizando mostradores
        canvas.delete('PRESS1')
        canvas.delete('PRESS2')
        alt_press1 = 175 - 1.5*int(gd.PRESS1)
        alt_press2 = 175 - 1.5*int(gd.PRESS2)
        canvas.create_rectangle(350,alt_press1,380,175,fill = "red",outline = "#DDD", tag='PRESS1')
        canvas.create_rectangle(380,alt_press2,410,175,fill = "red",outline = "#DDD", tag='PRESS2') 


    # Configurações de aparência do gráfico
    style.use('fivethirtyeight')
    graficos.tight_layout()

    # ----------------------------------------------------------------------------

    # Adicionando figuras à interface do tkinter
    canvas_VEL = FigureCanvasTkAgg(graficos, bt.area_graficos)
    canvas_VEL.draw()
    canvas_VEL.get_tk_widget().grid(row=0, column=0)   

    # Chama função que anima o gráfico
    ani = animation.FuncAnimation(graficos, animate, interval=1)

    # Executa a janela
    Interface.mainloop() 

 # ----------------------------------------------------------------------------

def entrada_do_usuario():
    '''
        Esta função recebe entradas do usuário. Através dela o usuário pode encerrar o programa, ou alternar entre o funcionamento 
        e a desativação da porta serial. 

    '''

    #global flag

    t1 = 'stop'  # ou 'start'
    t2 = 'parar'  # ou 'iniciar'
    t3 = 'em funcionamento'  # ou 'desativada'

    while 1:

        txt = 'Digite \"close\" para sair do programa ou \"%s\" para %s a leitura da porta serial: ' % (t1, t2)

        # nota-se que na primeira execução, a porta serial está aberta

        x1 = input(txt)

        #Resposta inválida:   ---------------------------------------------------
        while x1 != 'close' and x1 != t1:

            if x1 == 'stop' or x1 == 'start':
                print('\n >> A porta serial já está %s\n' % t3)
                x1 = input(txt)

            elif x1 != 'stop' or x1 != 'start':
                print("\n >> resposta inválida !\n")
                x1 = input(txt)

        # foi verificado que x1 ou é "close" ou a outra entrada válida.

        #Resposta "close" (em que o usuário fecha o programa): ------------------
        if x1 == 'close':

            cds.flag = 1  # Para o while da função coleta_de_dados

            print('\n \n VOCÊ FINALIZOU O PROGRAMA ! \n')
            os._exit(1)  # Fecha o programa

        #Outras entradas válidas (e que não fecham o programa):   ----------------
        # A) Caso em que a porta serial está em funcionamento (e o usuário para a leitura da porta serial):
        elif x1 == 'stop':

            cds.flag = 1  # Para o while da função coleta_de_dados
            print('\n >> A coleta de dados foi interrompida\n')

            t1 = 'start'
            t2 = 'iniciar'
            t3 = 'desativada'

        # B) Caso em que a porta serial está desativada (e o usuário a reativa):
        elif x1 == 'start':

            cds.flag = 0  # reinicia o funcionamento do while da função coleta_de_dados
            print('\n >> A coleta de dados foi reestabelecida\n')

            t1 = 'stop'
            t2 = 'parar'
            t3 = 'em funcionamento'

 #  ----------------------------------------------------------------------------

# Inicializando processos: -------------------------------------------------

def iniciar_processos():

    p_gerar = threading.Thread(target=gd.gerar_dados_aleatorios, name='Dados aleatórios')
    p_coleta = threading.Thread(target=cds.coleta_de_dados, name="Coleta de dados da serial", args=([9600]))
    p_user = threading.Thread(target=entrada_do_usuario, name="Processo de interface de usuário")

    p_gerar.start()
    user_interface()

iniciar_processos()

#Notas: ------------------------------------------------
'''
NOTE:
'''
