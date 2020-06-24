import matplotlib
matplotlib.use('TkAgg') # matplotlib no tkinter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation # a matplotlib é responsável por plotar gráficos

# Tela do módulo TkAgg onde serão plotados os graficos e a NavigationTollbar do matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import random 
from itertools import count # implementa contador do eixo x dos gráficos
import threading

import time

import tkinter as tk
from tkinter import *
from tkinter import ttk
#==================================================




# Definindo variáveis globais
x_eixo = VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = 0

def gerar_dados_aleatorios():

    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, HV

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
        time.sleep(1)
   


 #  ----------------------------------------------------------------------------


def grafico():

    # Definindo dimensões do gráfico (eixos)
    x_eixo = []
    y_VEL = []

    contador = count()

    # Função que anima o gráfico
    def animate(i):

        global VEL

        # Atualizando valores
        x_eixo.append(next(contador))
        y_VEL.append(VEL)
        
        # clear axes (limpa o gráfico entre um frame e outro)
        plt.cla()  

        # Plotando variáveis no gráfico
        plt.plot(x_eixo, y_VEL, label='Velocidade')
        plt.legend(loc='upper left')  


    # Configurações de aparência do gráfico
    plt.style.use('fivethirtyeight')

    # Chama função que anima o gráfico
    ani = FuncAnimation(plt.gcf(), animate, interval=1)
    plt.show()

 #  ----------------------------------------------------------------------------


def processos_paralelos():
    p_gerar = threading.Thread(target=gerar_dados_aleatorios, name='Dados aleatórios')
    p_graf2 = threading.Thread(target=grafico, name='Gráfico em tempo real')

    p_gerar.start()
    p_graf2.start()

 #  ----------------------------------------------------------------------------

processos_paralelos()

# gerar_dados_aleatorios()