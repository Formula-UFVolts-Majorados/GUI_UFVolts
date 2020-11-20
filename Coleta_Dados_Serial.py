import Gerador_de_Dados as gd
import serial # usada para leitura da porta serial
import os # usada para: encerrar o programa e pegar o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # usada para pegar o dado de tempo atual do computador


status = flag = 0

path = os.path.dirname(os.path.abspath(__file__))
diretorio = '%s\\Dados da telemetria.txt' % path

def coleta_de_dados(baud_rate):

    '''
        Esta função lê a porta serial COM2, armazena os dados recebidos em um txt e os separa em suas respectivas variáveis, 
    para que possam ser disponibilizados na interface gráfica por uma outra função.

    '''
    
    #global diretorio, flag, status
    #global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV

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

                gd.VEL = sd_list[0] + sd_list[1] + sd_list[2] 
                gd.APPS = sd_list[3] + sd_list[4] + sd_list[5] 
                gd.TM = sd_list[6] + sd_list[7] + sd_list[8]  
                gd.IMD = sd_list[9] 
                gd.BMS = sd_list[10] 
                gd.BSPD = sd_list[11]
                gd.PRESS1 = sd_list[12] + sd_list[13] 
                gd.PRESS2 = sd_list[14] +sd_list[15] 
                gd.HV = sd_list[16] + sd_list[17] + sd_list[18] 

                PRESS = (int(gd.PRESS1) + int(gd.PRESS2))*0.5
                
                # Salva os dados no txt
                with open(diretorio, 'a') as TXT:

                    current_time = str(datetime.now())
                    TXT.write(serialData + ' <> ' + current_time + '\n') 

 #  -----------------------------------------------