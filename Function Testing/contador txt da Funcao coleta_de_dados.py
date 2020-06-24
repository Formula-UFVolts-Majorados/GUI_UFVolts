import os # biblioteca com funções: encerra o programa e pega o caminho do arquivo deste programa no sistema operacional

# pegando a informação de path do próprio arquivo .py que está sendo executado
path = os.path.dirname(os.path.abspath(__file__))
# Criando uma string que contém o diretório do arquivo .txt que será criado no mesmo lugar do .py que está sendo executado
diretorio = '%s\\Dados da telemetria.txt' % path

#=========================================================================================================


# NOTE: Pretendo fazer um numerador para o TXT aqui, que printa "Coleta de Dados: X"
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