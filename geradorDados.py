import random # usada na função de testes

# Variáveis que armazenam os dados recebidos:
VEL = APPS = TM = IMD = BMS = BSPD = PRESS1 = PRESS2 = HV = RTD = 0

def gerarDadosAleatorios():
    global VEL, APPS, TM, IMD, BMS, BSPD, PRESS1, PRESS2, HV, RTD

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
        RTD = random.choice(list)

        # Dados do nível da bateria do HV
        aux1 = random.randrange(2)
        bateria = bateria - aux1 
        if bateria > 0 :
            HV = bateria
        else:
            HV = 0   

        # Dados da temperatura do motor
        aux2 = random.random()
        temperatura = temperatura + aux2/2
        if temperatura < 60:
            TM = temperatura
        else:
            TM = 60

        # Dados da velocidade
        aux3 = random.triangular(-3,3,0)
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

        print(end=" ")  
        
 #  ----------------------------------------------------------------------------