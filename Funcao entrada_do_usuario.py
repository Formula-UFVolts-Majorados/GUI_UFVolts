
import sys # biblioteca com função que encerra o programa.

def entrada_do_usuario():

    #  Esta função recebe uma entrada do usuário. Através dela o usuário pode encerrar o programa, ou alternar entre o funcionamento 
    #e a desativação da porta serial. 

    t1 = 'stop' # ou 'start'
    t2 = 'parar' # ou 'iniciar'
    t3 = 'em funcionamento' # ou 'desativada'
    

    while 1:

        txt = 'Digite \"close\" para sair do programa ou \"%s\" para %s a leitura da porta serial: ' %(t1,t2)

        x1 = input(txt)

        #Resposta inválida:
        while x1 != 'close' and x1 != t1:

            if x1 == 'stop' or x1 == 'start':
                print('A porta serial já está %s.'%t3)
                x1 = input(txt)
                

            elif x1 != 'stop' or x1 != 'start':
                print("resposta inválida !")
                x1 = input(txt)

        # foi verificado que x1 ou é "close" ou a outra entrada válida.


        #Resposta "close":  
        if x1 == 'close':

            print('para a coleta de dados')
            print('porta serial fechada')
            sys.exit('Você encerrou o programa !') # Fecha o programa


        #Outras entradas válidas:
        # A) Caso em que a porta serial está em funcionamento:
        elif x1 == 'stop':

            print('para a coleta de dados na porta serial')
            print('porta serial fechada')
            t1 = 'start'
            t2 = 'iniciar'
            t3 = 'desativada'
            
            
        # B) Caso em que a porta serial está desativada:
        elif x1 == 'start':

            print('porta serial abre')      
            t1 = 'stop'
            t2 = 'parar'
            t3 = 'em funcionamento'

entrada_do_usuario()
