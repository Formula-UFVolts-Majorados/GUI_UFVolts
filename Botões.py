#from GUI_UFVolts import graf_select, area_graficos, area_mostradores, legenda, janela_config

graf_select = area_graficos = area_mostradores = legenda = janela_config = 0

#Botões: -----------------------------------------------------------

class Funcoes():
    global graf_select, area_graficos, area_mostradores, legenda, janela_config

    def bt1_click(graf_select):
        if graf_select == 1:
            graf_select = 0
        print('bt1_click')
    def bt2_click(graf_select):
        if graf_select == 0:
            graf_select = 1
        print('bt2_click')
    def bt3_click(area_graficos, area_mostradores, legenda, janela_config): 
        area_graficos.pack(side='top', fill="both", expand=1)
        area_mostradores.pack(side='bottom', fill="x")
        legenda.pack_forget()
        janela_config.pack_forget()
        print("bt3_click")

    def bt4_click(area_graficos, area_mostradores, legenda, janela_config): 
        area_graficos.pack_forget()
        area_mostradores.pack_forget()
        legenda.pack_forget()
        janela_config.pack(side='top', fill="both", expand=1)
        print("bt4_click")

    def bt5_click(area_graficos, area_mostradores, legenda, janela_config):
        area_graficos.pack_forget()
        area_mostradores.pack_forget()
        janela_config.pack_forget()
        legenda.pack(side='left')
        print("bt5_click")

class Botoes(Funcoes):
    def __init__(self):
        self.criando_botoes
    
    def criando_botoes(self):
        bt1 = Button(lateral_bar, width=7, height=3, text="G1-VEL", command=self.bt1_click)
        bt2 = Button(lateral_bar, width=7, height=3, text="G1-TEMP", command=self.bt2_click)
        bt3 = Button(lateral_bar, width=7, height=3, text="MENU", command=self.bt3_click)
        bt4 = Button(lateral_bar, width=7, height=3, text="CONF", command=self.bt4_click)
        bt5 = Button(lateral_bar, width=7, height=3, text="LEGEN", command=self.bt5_click)
    
        bt1.grid(row=0, column=0, pady=(0,10))
        bt2.grid(row=1, column=0, pady=(0,10))
        bt3.grid(row=2, column=0, pady=(0,10))
        bt4.grid(row=3, column=0, pady=(0,10))
        bt5.grid(row=4, column=0, pady=(0,10))
   
Botoes()
