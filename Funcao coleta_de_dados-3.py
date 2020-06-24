import serial # permite a leitura da porta serial e registro em um .txt
import threading # permite a execução de atividades de forma paralela
import time # conta o tempo de execução do código
import os # biblioteca com funções: encerra o programa e pega o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # pega o dado de tempo atual do computador

#Variáveis globais:
# ------------------------------------------------
# pegando a informação de path do próprio arquivo .py que está sendo executado
path = os.path.dirname(os.path.abspath(__file__))
diretorio =  '%s\\Dados da telemetria.txt'%path # Criando uma string que contém o diretório do arquivo .txt que será criado no mesmo lugar do .py que está sendo executado
flag = 0 #Flag do while da função coleta_de_dados
VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = ''     # variáveis que armazenam os dados recebidos
#-------------------------------------------------

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


def coleta_de_dados(baud_rate):
    
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
    TXT = open(diretorio, "a+") 
    TXT.seek(0,0) 

    coletas = TXT.readline(1) 

    if coletas == '': 

        TXT.write('1 coleta armazenada\n')
        TXT.write('\nColeta de Dados nº1 \n')

    elif coletas != '':

        coletas = int(coletas) 
        coletas += 1  

        lines = TXT.readlines() 

        with open(diretorio, "w") as TXT:

            lines[0] = ('%s coletas armazenadas\n' %coletas) 
            
            for line in lines:
                TXT.write(line) 
    
        with open(diretorio, "a") as TXT: 
            TXT.write('\nColeta de Dados nº%s \n' %coletas)

    TXT.close()
    

    # Looping principal da função:
    while 1:
        while flag != 1:
        
            serialByte = PSERIAL.read(1).decode('ascii')

            if serialByte == '-':
                
                serialData = PSERIAL.read(number_of_bytes).decode('ascii')
 

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
                

                with open(diretorio, 'a') as TXT:

                    current_time = str(datetime.now())
                    TXT.write(serialData + ' <> ' + current_time + '\n') 

 #  -----------------------------------------------
        

                
       
coleta_de_dados(9600)









