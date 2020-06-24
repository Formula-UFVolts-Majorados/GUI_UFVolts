import matplotlib
matplotlib.use('TkAgg') # matplotlib no tkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Tela do módulo TkAgg onde serão plotados os graficos e a NavigationTollbar do matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style

import random 
from itertools import count # implementa contador do eixo x dos gráficos
import threading

import time

import tkinter as tk
from tkinter import *
from tkinter import ttk
#======================================================================================


# Definindo variáveis globais
x_eixo = VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = fig = 0

def gerar_dados_aleatorios():

    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV

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

        print(VEL)  
        
 #  ----------------------------------------------------------------------------


def user_interface():

    # Define a janela principal (objeto) da aplicação
    menu_inicial = Tk()  

    # Definindo características da janela
    menu_inicial.title('Telemetria UFVolts Majorados')
    menu_inicial.state('zoomed')  # define que a janela fique em tela cheia
    menu_inicial.iconbitmap('images\icon.ico')
    menu_inicial['bg'] = '#%02x%02x%02x' %(200, 34, 34) # definindo a cor de fundo da janela (bg = background)

    # Inserindo imagens
    imagem_logo = PhotoImage(file="images\logoformula1.png") # importando imagem
    logoformula = Label(menu_inicial, image=imagem_logo, borderwidth=0) #label com imagem
    # logoformula.place(x=1150, y=600) #localização da imagem
    logoformula.pack(side=BOTTOM, anchor=SE)

    # Criando botões

    # Adicionando texto (labels)

    # ADICIONANDO GRÁFICOS ----------------------------------------------------

    # Definindo dimensões do gráfico (eixos)
    x_eixo = []
    y_VEL = []

    # Contador do eixo x
    contador = count()

    # Criando figura que será printada na interface do tkinter
    fig_VEL = Figure(figsize=(3.8,3.8), dpi=100)
    subplot = fig_VEL.add_subplot(111)

    # Função que anima o gráfico
    def animate(i):

        global VEL

        # Atualizando valores
        x_eixo.append(next(contador))
        y_VEL.append(VEL)

        if len(x_eixo) > 50:
            aux = y_VEL.pop(0)
            aux = x_eixo.pop(0)

        # clear axes (limpa o gráfico entre um frame e outro)
        subplot.cla()  

        # Plotando variáveis no gráfico
        subplot.plot(x_eixo, y_VEL, label='Velocidade')
        subplot.legend(loc='upper left')

    # Configurações de aparência do gráfico
    style.use('fivethirtyeight')

    # ----------------------------------------------------------------------------

    # Adicionando figuras à interface do tkinter
    canvas_VEL = FigureCanvasTkAgg(fig_VEL, menu_inicial)
    canvas_VEL.draw()
    canvas_VEL.get_tk_widget().pack(side=BOTTOM, anchor=S)    #place(x=500, y=300)     

    # Chama função que anima o gráfico
    ani = animation.FuncAnimation(fig_VEL, animate, interval=1)
    
    # Executa a janela
    menu_inicial.mainloop()  
 #  -----------------------------------------------


def processos_paralelos():
    p_gerar = threading.Thread(target=gerar_dados_aleatorios, name='Dados aleatórios')
    p_UI = threading.Thread(target=user_interface, name='Interface de Usuário')

    p_gerar.start()
    p_UI.start()
 #  ----------------------------------------------------------------------------

processos_paralelos()
