#from GUI_UFVolts import graf_select, area_graficos, area_mostradores, legenda, janela_config

graf_select = area_graficos = area_mostradores = legenda = janela_config = 0

#Botões: -----------------------------------------------------------

def bt1_click():
    global graf_select
    if graf_select == 1:
        graf_select = 0
    print("bt1_click") 

def bt2_click():
    global graf_select
    if graf_select == 0:
        graf_select = 1
    print("bt2_click")

def bt3_click():
    global area_graficos, area_mostradores, legenda, janela_config
    area_graficos.pack(side='top', fill="both", expand=1)
    area_mostradores.pack(side='bottom', fill="x")
    legenda.pack_forget()
    janela_config.pack_forget()
    print("bt3_click")

def bt4_click():
    global area_graficos, area_mostradores, legenda, janela_config
    area_graficos.pack_forget()
    area_mostradores.pack_forget()
    legenda.pack_forget()
    janela_config.pack(side='top', fill="both", expand=1)
    print("bt4_click")

def bt5_click():
    global area_graficos, area_mostradores, legenda, janela_config
    area_graficos.pack_forget()
    area_mostradores.pack_forget()
    janela_config.pack_forget()
    legenda.pack(side='left')
    print("bt5_click")
