import serial # trabalha com a porta serial
import pathlib # pega o caminho do arquivo deste programa no sistema operacional
from datetime import datetime # pega o dado de tempo atual do computador

#Variáveis globais:
# ------------------------------------------------
path = pathlib.Path(__file__).parent.absolute() # pegando a informação de path do próprio arquivo .py que está sendo executado
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
    '''
        Esta função abre uma porta serial PSERIAL e lê a informação que está sendo recebida. Ela tem como argumento o número de bytes
    que lerá e armazenará em um arquivo .txt externo e seu baud rate (taxa de transmissão). Ela lê os bytes de dados a partir de um 
    handshake ('-').

    '''
    
    global PSERIAL, diretorio, flag
    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV

    PSERIAL = serial.Serial('COM2', baudrate=baud_rate,
                            timeout=2)  # abrindo porta serial

    # NOTE: Posso eliminar o argumento de baudrate ? O que isso implicaria ?

    # Esta seção conta o número de bytes que estão sendo recebidos 
    # e armazena esse número na variável "number_of_bytes
    # ========================================================
    serialByte = PSERIAL.read_until('-').decode('ascii') # encontra o handshake ('-')

    serialByte = ''
    number_of_bytes = -1
    
    # conta os bytes até o próximo hanshake
    while serialByte != '-':
        serialByte = PSERIAL.read(1).decode('ascii')
        number_of_bytes += 1

    print(number_of_bytes)
   
    # Esta seção cria um contador de registros para o txt 
    # ================================
    TXT = open(diretorio, "a+") # abre o TXT em modo "acrescentar"(append), o criando se não existir
    TXT.seek(0,0) # vai para o começo do arquivo

    coletas = TXT.readline(1) # lê o primeiríssimmo byte do arquivo (que será um número)



    # se o arquivo foi criado e estiver vazio, salva as informações iniciais
    if coletas == '': 

        TXT.write('1 coleta armazenada\n')
        TXT.write('\nColeta de Dados nº1 \n')

    # se o arquivo não estiver vazio
    elif coletas != '':

        coletas = int(coletas) # transforma o número em formato str para o formato int
        coletas += 1  # adiciona mais uma unidade de coleta

        lines = TXT.readlines() # lê todo o .txt e o armazena na lista "lines"

        with open(diretorio, "w") as TXT:

            lines[0] = ('%s coletas armazenadas\n' %coletas) # substitui a primeira linha
            
            for line in lines:
                TXT.write(line) # reescreve o txt com as mudanças
    
        with open(diretorio, "a") as TXT: 
            TXT.write('\nColeta de Dados nº%s \n' %coletas) # acrescenta o rótulo de coleta

    TXT.close()
    
    # ===============================


    # Looping principal da função:
    while 1:
        while flag != 1:
        
            serialByte = PSERIAL.read(1).decode('ascii')

            if serialByte == '-':
                # lê os próximos x bytes, tal que x será indicado como um argumento da função coleta_de_dados
                serialData = PSERIAL.read(number_of_bytes).decode('ascii')

                print(number_of_bytes)


                # NOTE: Há alguma função que já leia direto entre dois handshakes (-0...0000- ) ?  

                print(serialData)

                #-> Separando os dados de cada byte dentro da string: -VVV APP TMT IBB P1 P2 BHV, 
                # e os salvando em uma lista e em variáveis prórpias:

                sd_list = list(serialData)

                VEL = sd_list[0] + sd_list[1] + sd_list[2] # velocidade do carro
                APPS = sd_list[3] + sd_list[4] + sd_list[5] # posição do pedal
                TM = sd_list[6] + sd_list[7] + sd_list[8]  # temperatura do motor
                IMD = sd_list[9] # sinal de dois estados que indica falha no IMD 
                BMS = sd_list[10] # sinal de dois estados que indica falha no BMS 
                BSPD = sd_list[11] # sinal de dois estados que indica falha no BSPD
                PRESS1 = sd_list[12] + sd_list[13] # 1ª leitura da pressão no fluido de freio
                PRESS2 = sd_list[14] +sd_list[15] # 2ª leitura da pressão no fluido de freio
                HV = sd_list[16] + sd_list[17] + sd_list[18] # carga da bateria no sistema de alta tensão do carro


                #-> Salvando os dados em um TXT externo para registro:
                with open(diretorio, 'a') as TXT:

                    # cria uma string com o tempo atual do PC
                    current_time = str(datetime.now())
                    TXT.write(serialData + ' <> ' +
                                current_time + '\n')  # salva no .txt

 #  -----------------------------------------------
        

                
       
coleta_de_dados(9600)









