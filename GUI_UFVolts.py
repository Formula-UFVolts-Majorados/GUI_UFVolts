'''
\\\\\\UFVOLTS MAJORADOS////////

Acompanhamento dos dados em tempo real do protótipo FSAE recebidos via rádio, coletados pelo módulo HC-12
Simulação realizada com o auxílio dos softwares:
-Virtual Serial Ports Emulator
-Proteus (esquemática de circuito com código para o PIC)

Autor: Déric Augusto - Eletrônica 2
       Sandro Manoel - Eletrônica 
       Mayelli Costa - Eletrônica
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

import serial # usada para leitura da porta serial
import threading # usada para execução de atividades de forma paralela
import time # usada para testes
import os # usada para: encerrar o programa e pegar o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # usada para pegar o dado de tempo atual do computador
import random # usada na função de testes
from itertools import count # implementa contador do eixo x dos gráficos
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation # a matplotlib é responsável por plotar gráficos

#Variáveis globais:
#-------------------------------------------------
# String que define o .txt onde serão armazenados os dados
path = os.path.dirname(os.path.abspath(__file__))
diretorio = '%s\\Dados da telemetria.txt' % path
# Flag do while da função coleta_de_dados:
flag = 0
# Variáveis que armazenam os dados recebidos:
VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = ''
#-------------------------------------------------

#Funções:

def teste_gera_dados():

    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV

    '''
    VEL (velocidade) -> vai de 0 à 90km/h de forma suave, sendo que geralmente oscila entre 20 e 30km/h
    APPS ->  ?
    TM (temperatura do motor) ->  ?
    IMD -> 0 ou 1
    BMS -> 0 ou 1
    BSPD -> 0 ou 1
    PRESS1\PRESS2 -> ?
    HV ->  ?
    '''

    VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = 0

    while 1: 
        VEL += random.randint(-2,2)
        APPS += random.randint(-6,8)
        TM += random.randint(-1,1)
        IMD += random.randint(-6,8)
        BMS += random.randint(-6,8)
        BSPD += random.randint(-6,8)
        PRESS1 += random.randint(-10,8)
        PRESS2 += random.randint(-6,10)
        HV += random.randint(-6,8)


def grafico():

    # Definindo dimensões do gráfico (eixos)
    x_eixo = []
    y_VEL = []
    y_APPS = []
    y_TM = []
    y_PRESS1 = []
    y_PRESS2 = []
    y_HV = []

    contador = count()

    # Função que anima o gráfico
    def animate(i):

        global VEL, APPS, TM, PRESS1, PRESS2, HV

        x_eixo.append(next(contador))
        y_VEL.append(VEL)
        y_APPS.append(APPS)
        y_TM.append(TM)
        y_PRESS1.append(PRESS1)
        y_PRESS2.append(PRESS2)
        y_HV.append(HV)
        

        plt.cla()  # clear axes (limpa o gráfico entre um frame e outro)

        plt.plot(x_eixo, y_VEL, label='Velocidade')
        plt.plot(x_eixo, y_APPS, label='APPS')
        plt.plot(x_eixo, y_TM, label='T. do Motor')
        plt.plot(x_eixo, y_PRESS1, label='PRESS1')
        plt.plot(x_eixo, y_PRESS2, label='PRESS2')
        plt.plot(x_eixo, y_HV, label='HV')

        plt.legend(loc='upper left')  

    # Configurações de aparência do gráfico
    plt.style.use('fivethirtyeight')
    plt.tight_layout()

    # Chama função que anima o gráfico
    ani = FuncAnimation(plt.gcf(), animate, interval=1)

    plt.show()

 #  ----------------------------------------------------------------------------

p_grafico = threading.Thread(target=grafico, name="Gráfico")

def coleta_de_dados(baud_rate):

    '''
        Esta função lê a porta serial COM2, armazena os dados recebidos em um txt e os separa em suas respectivas variáveis, 
    para que possam ser disponibilizados na interface gráfica por uma outra função.

    '''
    
    global diretorio, flag
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
        while flag != 1:
        
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

p_coleta = threading.Thread(target=coleta_de_dados, name="Coleta de dados da serial", args=([9600]))

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

p_user = threading.Thread(target=entrada_do_usuario, name="Processo de interface de usuário")





# Inicializando processos:
#  -------------------------------------------------
p_user.start()
p_coleta.start()
p_grafico.start()

# -----------------------------------------------

#Notas:
#------------------------------------------------
'''
NOTE:
'''
