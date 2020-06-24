import random
import time


sinal = [("0", 1), ("1", 50)]                                  
list = [prize for prize, weight in sinal for i in range(weight)]
bat = 100
temp = random.uniform(24,25)
vel = 40
pres = 5

while 1:
    I = random.choice(list)
    B1 = random.choice(list)
    B2 = random.choice(list)

    aux1 = random.randrange(2)
    bat = bat - aux1 
    if bat > 0 :
        BHV = bat
    else:
        BHV = 0   

    aux2= random.random()
    temp = temp + aux2/2
    if temp < 60:
        TMT = temp
    else:
        TMT = 60

    aux3=random.triangular(-3,3,0)
    vel = vel + aux3
    if 0 < vel < 90:
        VVV = vel

    aux4 = random.uniform(-3,3)
    pres = pres + aux4
    if 0 < pres <= 80:
        P1 = pres
    if -2 < pres < 0:
        P1 = P2 = random.uniform(60,70)
    if -4 < pres < -2:
        P1 = P2 = random.uniform(0,3)
    if pres <= -4:
        P1 = P2 = random.uniform(50,70)
    if pres > 80:
        P1 = P2 = random.uniform(0,10)    
    if 0 < pres < 2:
        P2 = pres 
    if 2 <= pres < 10:
        P2 = pres - random.random()
    if 10 <= pres <= 80:
        P2 = pres - random.uniform(0,5)  
    APP = (P1 + P2) /2 * 1.25
    
    print(I,B1,B2,BHV,TMT,VVV,P1,P2,APP)
    time.sleep(0.5)
    

