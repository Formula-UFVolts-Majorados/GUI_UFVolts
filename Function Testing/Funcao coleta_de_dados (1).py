import serial # trabalha com a porta serial
import pathlib # pega o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # pega o dado de tempo atual do computador

#Variáveis globais:
# ------------------------------------------------
path = pathlib.Path(__file__).parent.absolute() # pegando a informação de path do próprio arquivo .py que está sendo executado
diretorio =  '%s\\Dados da telemetria.txt'%path # Criando uma string que contém o diretório do arquivo .txt que será criado no mesmo lugar do .py que está sendo executado
flag = 0 #Flag do while da função coleta_de_dados
#-------------------------------------------------

def coleta_de_dados(number_of_bytes):

    '''
        Esta função abre uma porta serial PSERIAL e lê a informação que está sendo recebida. Ela tem como argumento o número de bytes
    que lerá e armazenará em um arquivo .txt externo. Ela lê os bytes de dados através de um handshake ('-').

    '''

    print('A função coleta_de_dados foi iniciada') # XXX APENAS PARA ACOMPANHAR O QUE ACONTECE NO CÓDIGO

    global diretorio
    global flag

    PSERIAL = serial.Serial('COM2', baudrate = 57600, timeout=2)  # abrindo porta serial

    with open(diretorio,"a") as TXT:
        TXT.write('\nColeta de Dados: A \n')

    while flag != 1:

        serialByte = PSERIAL.read(1).decode('ascii') # lê byte por byte recebido da porta serial no formato 'byte'(b'') e o converte para uma string('')
        
        if serialByte == '-': # encontra o handshake
            
            serialData = PSERIAL.read(number_of_bytes).decode('ascii') # lê os próximos x bytes, tal que x será indicado como um argumento da função coleta_de_dados
            
            with open(diretorio,'a') as TXT:

                current_time = str(datetime.now()) # cria uma string com o tempo atual do PC
                TXT.write(serialData + ' <> ' + current_time + '\n')  # salva no .txt    

                #  print(serialData + ' <> ' + current_time) # XXX APENAS PARA ACOMPANHAR O QUE ACONTECE NO CÓDIGO

    #  -----------------------------------------------
        

                
       
coleta_de_dados(3)











