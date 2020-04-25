'''
\\\\\\UFVOLTS MAJORADOS////////

Acompanhamento dos dados em tempo real do protótipo FSAE recebidos via rádio, coletados pelo módulo HC-12
Simulação realizada com o auxílio dos softwares:
-Virtual Serial Ports Emulator
-Proteus (esquemática de circuito com código para o PIC)

Autor: Déric Augusto - Eletrônica
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

import serial # permite a leitura da porta serial e registro em um .txt
import threading # permite a execução de atividades de forma paralela
import time # conta o tempo de execução do código
import os # biblioteca com funções: encerra o programa e pega o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # pega o dado de tempo atual do computador

#Variáveis globais:
# ------------------------------------------------
# pegando a informação de path do próprio arquivo .py que está sendo executado
path = os.path.dirname(os.path.abspath(__file__))
# Criando uma string que contém o diretório do arquivo .txt que será criado no mesmo lugar do .py que está sendo executado
diretorio = '%s\\Dados da telemetria.txt' % path
flag = 0  # Flag do while da função coleta_de_dados
PSERIAL = 1  # Indicando como uma variável global
#-------------------------------------------------

#Funções:
# ------------------------------------------------


def coleta_de_dados(number_of_bytes, baud_rate):
    '''
        Esta função abre uma porta serial PSERIAL e lê a informação que está sendo recebida. Ela tem como argumento o número de bytes
    que lerá e armazenará em um arquivo .txt externo e seu baud rate (taxa de transmissão). Ela lê os bytes de dados a partir de um 
    handshake ('-').

    '''

    global PSERIAL, diretorio, flag

    PSERIAL = serial.Serial('COM2', baudrate=baud_rate,
                            timeout=2)  # abrindo porta serial

    with open(diretorio, "a") as TXT:
        TXT.write('\nColeta de Dados: A \n')

    while 1:
        while flag != 1:

            # lê byte por byte recebido da porta serial no formato 'byte'(b'') e o converte para uma string('')
            serialByte = PSERIAL.read(1).decode('ascii')

            if serialByte == '-':  # encontra o handshake

                # lê os próximos x bytes, tal que x será indicado como um argumento da função coleta_de_dados
                serialData = PSERIAL.read(number_of_bytes).decode('ascii')

                with open(diretorio, 'a') as TXT:

                    # cria uma string com o tempo atual do PC
                    current_time = str(datetime.now())
                    TXT.write(serialData + ' <> ' +
                              current_time + '\n')  # salva no .txt

 #  -----------------------------------------------


def entrada_do_usuario():
    '''

        Esta função recebe entradas do usuário. Através dela o usuário pode encerrar o programa, ou alternar entre o funcionamento 
    e a desativação da porta serial. 

    '''

    global PSERIAL, flag

    t1 = 'stop'  # ou 'start'
    t2 = 'parar'  # ou 'iniciar'
    t3 = 'em funcionamento'  # ou 'desativada'

    while 1:

        txt = 'Digite \"close\" para sair do programa ou \"%s\" para %s a leitura da porta serial: ' % (
            t1, t2)

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


def iniciar_processos_paralelos():

    # definindo as funções dadas processos:
    p_coleta = threading.Thread(
        target=coleta_de_dados, name="Coleta de dados da serial", args=([19, 9600]))
    p_user = threading.Thread(
        target=entrada_do_usuario, name="Processo de interface de usuário")

    # startando os processos (as theadings):
    p_user.start()
    p_coleta.start()

 #  -------------------------------------------------

# -----------------------------------------------


iniciar_processos_paralelos()


#Notas:
#------------------------------------------------
'''
NOTE:
'''
