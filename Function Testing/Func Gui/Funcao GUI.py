import tkinter as tk
from tkinter import *
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg') # matplotlib no tkinter

# Tela do módulo TkAgg onde serão plotados os graficos e a NavigationTollbar do matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure 



def user_interface():

    menu_inicial = Tk()  # define a janela principal (objeto) da aplicação

    # Definindo características da janela

    menu_inicial.title('Telemetria UFVolts Majorados')
    menu_inicial.state('zoomed')  # define que a janela fique em tela cheia
    # menu_inicial.resizable(False, False) # não permite que o formato da janela seja alterado em nehuma direção
    #menu_inicial.iconbitmap('images\icon.ico')
    menu_inicial['bg'] = '#%02x%02x%02x' %(200, 34, 34) # definindo a cor de fundo da janela (bg = background)

    # Inserindo imagens

    imagem_logo = PhotoImage(file="images\logoformula1.png") # importando imagem
    logoformula = Label(menu_inicial, image=imagem_logo, borderwidth=0) #label com imagem
    logoformula.place(x=1150, y=600) #localização da imagem

    # Criando botões






    # Adicionando texto (labels)



    # Adicionando gráficos
    

    # - criando figura que contém o gráfico
    fig = Figure(figsize=(3.8,3.8), dpi=100)
    
    ax = fig.add_subplot(111) # gráfico 1por 1. Gráfico nº1
    ax.grid() #Fundo quadriculado
    ax.set_xlabel("Tempo") #Nome da coordenada x
    ax.set_ylabel("Velocidade") #Nome da coordenada y
    ax.plot([1,2,3,4,5,],[1,3,4,5,2])

    # - adicionando figura à interface do tkinter
    canvas = FigureCanvasTkAgg(fig, master=menu_inicial)
    canvas.draw()
    canvas.get_tk_widget().place(x=500, y=300)       #.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

   



    menu_inicial.mainloop()  # executa a janela
 #  -----------------------------------------------

 

user_interface()