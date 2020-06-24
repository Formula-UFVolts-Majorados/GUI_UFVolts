import serial # trabalha com a porta serial
import pathlib # pega o caminho do arquivo deste programa no sistema operacional

#Variáveis globais:
# ------------------------------------------------
path = pathlib.Path(__file__).parent.absolute() # pegando a informação de path do próprio arquivo .py que está sendo executado
diretorio =  '%s\\Dados da telemetria.txt'%path # Criando uma string que contém o diretório do arquivo .txt que será criado no mesmo lugar do .py que está sendo executado
flag = 0 #Flag do while da função coleta_de_dados
#-------------------------------------------------



PSERIAL = serial.Serial('COM2', baudrate= 9600, timeout=2) 


serialByte = ''

while serialByte != '-':
    serialByte = PSERIAL.read(1).decode('ascii')     # acha o primeiro handshake

serialByte = ''
number_of_bytes = -1

while serialByte != '-':                             # acha o segundo handshake
    serialByte = PSERIAL.read(1).decode('ascii')
    number_of_bytes += 1

print(number_of_bytes)