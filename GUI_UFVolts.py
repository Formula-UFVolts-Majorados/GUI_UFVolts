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
import serial # usada para leitura da porta serial
import threading # usada para execução de atividades de forma paralela
import os # usada para: encerrar o programa e pegar o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # usada para pegar o dado de tempo atual do computador
import random # usada na função de testes
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
path = os.path.dirname(os.path.abspath(__file__))
diretorio = '%s\\Dados da telemetria.txt' % path

# Flag do while da função coleta_de_dados:
flag = 0

# Variáveis que armazenam os dados recebidos:
VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = RTD = 0

# Variáveis de objetos:
canvas = status = 0
subplot1 = subplot2 = 0
#area_graficos = area_mostradores = legenda = graf_select = janela_config =
# Definindo dimensões do gráfico (eixos)
x_eixo = []
y_VEL = []
y_TM = []
y_PRESS1 = []
y_PRESS2 = []
y_APPS = []
y_HV = []

#Funções: -----------------------------------------------------------

def gerar_dados_aleatorios():
    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV, RTD, canvas

    sinal = [("0", 1), ("1", 50)]                                  
    list = [prize for prize, weight in sinal for i in range(weight)]
    bateria = 100
    temperatura = random.uniform(24,25)
    vel = 40
    pressao = 5

    while 1:

        # Dados de dois estados dos componentes do Shutdown
        IMD = random.choice(list)
        BMS = random.choice(list)
        BSPD = random.choice(list)
        RTD = random.choice(list)

        # Dados do nível da bateria do HV
        aux1 = random.randrange(2)
        bateria = bateria - aux1 
        if bateria > 0 :
            HV = bateria
        else:
            HV = 0   

        # Dados da temperatura do motor
        aux2= random.random()
        temperatura = temperatura + aux2/2
        if temperatura < 60:
            TM = temperatura
        else:
            TM = 60

        # Dados da velocidade
        aux3=random.triangular(-3,3,0)
        vel = vel + aux3
        if 0 < vel < 90:
            VEL = vel

        # Dados das Pressões no fluido de freio
        aux4 = random.uniform(-3,3)
        pressao = pressao + aux4
        if 0 < pressao <= 80:
            PRESS1 = pressao
        if -2 < pressao < 0:
            PRESS1 = PRESS2 = random.uniform(60,70)
        if -4 < pressao < -2:
            PRESS1 = PRESS2 = random.uniform(0,3)
        if pressao <= -4:
            PRESS1 = PRESS2 = random.uniform(50,70)
        if pressao > 80:
            PRESS1 = PRESS2 = random.uniform(0,10)    
        if 0 < pressao < 2:
            PRESS2 = pressao 
        if 2 <= pressao < 10:
            PRESS2 = pressao - random.random()
        if 10 <= pressao <= 80:
            PRESS2 = pressao - random.uniform(0,5)  
        APPS = (PRESS1 + PRESS2) /2 * 1.25

        print(end=" ")  
        
 #  ----------------------------------------------------------------------------

def coleta_de_dados(baud_rate):

    '''
        Esta função lê a porta serial COM2, armazena os dados recebidos em um txt e os separa em suas respectivas variáveis, 
    para que possam ser disponibilizados na interface gráfica por uma outra função.

    '''
    
    global diretorio, flag, status
    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV

    PSERIAL = serial.Serial('COM2', baudrate=baud_rate, timeout=2) 

    # Conta o número de bytes que estão sendo recebidos
    # e armazena esse número na variável "number_of_bytes"
    serialByte = ''

    while serialByte != '-':
        serialByte = PSERIAL.read(1).decode('ascii')     

    serialByte = ''
    number_of_bytes = -1

    while serialByte != '-':                           
        serialByte = PSERIAL.read(1).decode('ascii')
        number_of_bytes += 1
   
    
    # Executa o contador do txt

    '''
        O contador do txt conta quantas coletas de dados foram realizadas. À cada vez que o programa é iniciado,
    é considerada uma coleta.

    '''
    TXT = open(diretorio, "a+") 
    TXT.seek(0,0) 

    coletas = TXT.readline(1) 

    if coletas == '': 

        TXT.write('1 coleta armazenada\n')
        TXT.write('\n' + '='*49 + '\n')
        TXT.write(' '*13 + 'Coleta de Dados nº1 \n')

    elif coletas != '':

        coletas = int(coletas) 
        coletas += 1  

        lines = TXT.readlines() 

        with open(diretorio, "w") as TXT:

            lines[0] = ('%s coletas armazenadas\n' %coletas) 
            
            for line in lines:
                TXT.write(line) 
    
        with open(diretorio, "a") as TXT: 
            TXT.write('\n' + '='*49 + '\n')
            TXT.write(' '*13 + 'Coleta de Dados nº%s \n' %coletas)

    TXT.close()
    

    # Looping principal da função:
    while 1:
        status.configure(text="Status: sem conexão", fg="red")
        
        while flag != 1:
            status.configure(text="Status: conectado", fg="green")

            serialByte = PSERIAL.read(1).decode('ascii')

            if serialByte == '-':
                
                serialData = PSERIAL.read(number_of_bytes).decode('ascii')
 
                # Separa os dados em suas respectivas variáveis
                sd_list = list(serialData)

                VEL = sd_list[0] + sd_list[1] + sd_list[2] 
                APPS = sd_list[3] + sd_list[4] + sd_list[5] 
                TM = sd_list[6] + sd_list[7] + sd_list[8]  
                IMD = sd_list[9] 
                BMS = sd_list[10] 
                BSPD = sd_list[11]
                PRESS1 = sd_list[12] + sd_list[13] 
                PRESS2 = sd_list[14] +sd_list[15] 
                HV = sd_list[16] + sd_list[17] + sd_list[18] 

                PRESS = (int(PRESS1) + int(PRESS2))*0.5
                
                # Salva os dados no txt
                with open(diretorio, 'a') as TXT:

                    current_time = str(datetime.now())
                    TXT.write(serialData + ' <> ' + current_time + '\n') 

 #  -----------------------------------------------

def user_interface():
    global subplot1, subplot2, canvas, status#, area_graficos, area_mostradores, janela_config, legenda

    # Define a janela principal (objeto) da aplicação
    Interface = Tk()  

    # Definindo características da janela
    Interface.title('Telemetria UFVolts Majorados')
    Interface.state('zoomed')  # define que a janela fique em tela cheia
    Interface.iconbitmap('images/icon.ico')
    Interface['bg'] = "black" #'#%02x%02x%02x' %(200, 34, 34) # definindo a cor de fundo da janela (bg = background)

    # Criando frames
    lateral_bar = LabelFrame(Interface, bg='#%02x%02x%02x' %(200, 34, 34), borderwidth=0, padx=10, pady=10)
    lateral_bar.pack(side=LEFT, fill="y")

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
    bt1 = Button(lateral_bar, width=7, height=3, text="G1-VEL", command=bt.bt1_click)
    bt2 = Button(lateral_bar, width=7, height=3, text="G1-TEMP", command=bt.bt2_click)
    bt3 = Button(lateral_bar, width=7, height=3, text="MENU", command=bt.bt3_click)
    bt4 = Button(lateral_bar, width=7, height=3, text="CONF", command=bt.bt4_click)
    bt5 = Button(lateral_bar, width=7, height=3, text="LEGEN", command=bt.bt5_click)
    
    bt1.grid(row=0, column=0, pady=(0,10))
    bt2.grid(row=1, column=0, pady=(0,10))
    bt3.grid(row=2, column=0, pady=(0,10))
    bt4.grid(row=3, column=0, pady=(0,10))
    bt5.grid(row=4, column=0, pady=(0,10))

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
    alt_press1 = 175 - 1.5*int(PRESS1)
    alt_press2 = 175 - 1.5*int(PRESS2)
    alt_BHV = 175 - 1.5*int(HV)
    alt_temp = 175 - 1.5*int(TM)
    alt_APPS = 50 + int(APPS)

    #  Adicionando barras gráficas e LEDS de estado
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    tk.Canvas.create_circle = _create_circle
    
    if IMD == "1":
        canvas.create_circle(1400, 35, 30, fill="green", outline="#DDD")
    else:
        canvas.create_circle(1400, 35, 30, fill="red", outline="#DDD")
    if BMS == "1":        
        canvas.create_circle(1400, 105, 30, fill="green", outline="#DDD")
    else:        
        canvas.create_circle(1400, 105, 30, fill="red", outline="#DDD")
    if BSPD == "1":        
        canvas.create_circle(1400, 175, 30, fill="green", outline="#DDD")
    else:        
        canvas.create_circle(1400, 175, 30, fill="red", outline="#DDD")
    if RTD == "1":        
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
        global VEL, TM, PRESS1, PRESS2, subplot1, subplot2#, graf_select

        #Tempo real para gráfico
        data_hora_atual = datetime.now()
        minuto_segundo_milisegundo = data_hora_atual.strftime('%M:%S.%f')[:-3]

        # Atualizando valores
        x_eixo.append(minuto_segundo_milisegundo)
        y_VEL.append(VEL)
        y_TM.append(TM)
        y_PRESS1.append(PRESS1)
        y_PRESS2.append(PRESS2)

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
        alt_press1 = 175 - 1.5*int(PRESS1)
        alt_press2 = 175 - 1.5*int(PRESS2)
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

    global flag

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

            flag = 1  # Para o while da função coleta_de_dados

            print('\n \n VOCÊ FINALIZOU O PROGRAMA ! \n')
            os._exit(1)  # Fecha o programa

        #Outras entradas válidas (e que não fecham o programa):   ----------------
        # A) Caso em que a porta serial está em funcionamento (e o usuário para a leitura da porta serial):
        elif x1 == 'stop':

            flag = 1  # Para o while da função coleta_de_dados
            print('\n >> A coleta de dados foi interrompida\n')

            t1 = 'start'
            t2 = 'iniciar'
            t3 = 'desativada'

        # B) Caso em que a porta serial está desativada (e o usuário a reativa):
        elif x1 == 'start':

            flag = 0  # reinicia o funcionamento do while da função coleta_de_dados
            print('\n >> A coleta de dados foi reestabelecida\n')

            t1 = 'stop'
            t2 = 'parar'
            t3 = 'em funcionamento'

 #  ----------------------------------------------------------------------------


# Inicializando processos: -------------------------------------------------

def iniciar_processos():

    p_gerar = threading.Thread(target=gerar_dados_aleatorios, name='Dados aleatórios')
    p_coleta = threading.Thread(target=coleta_de_dados, name="Coleta de dados da serial", args=([9600]))
    p_user = threading.Thread(target=entrada_do_usuario, name="Processo de interface de usuário")

    p_gerar.start()
    user_interface()

iniciar_processos()

#Notas: ------------------------------------------------
'''
NOTE:
'''
