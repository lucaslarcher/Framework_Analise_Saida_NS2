import sys
import matplotlib.pyplot as plt
import numpy as np

#LEITURA DO ARQUIVO

parametros = []
for param in sys.argv :
    parametros.append(param)
    

arquivo = ''
seed = ''
nome = ''
print(parametros)
if(len(parametros) != 1):
    arquivo = parametros[1]
    seed = parametros[1].split('_')
    seed = seed[2].split('.')[0]
    nome = (parametros[1].split('_')[0]).split('/')[1]
    sobrenome = (parametros[1].split('_')[0]+'_'+parametros[1].split('_')[1]).split('/')
    sobrenome = sobrenome[len(sobrenome)-1]
  

numPolos = 5
timeWork = 10*60*60
colorPolos = ['red','blue','green','yellow','orange']
numMaquinasPolo = [30,20,47,50,30]

pathSaida = "/home/lucas/Documents/ns2/graficos/"
subName = nome+"_"+seed+"_"


import os
import subprocess

#FUNCOES DE GERACAO DE GRAFICOS

def gerar_arquivo_leitura_GnuPlot(caminho,nomearquivo,vetorvetorX,vetorvetorY):
    for i in range(len(vetorvetorX)):
        print(caminho+nomearquivo+'_'+str(i)+'.txt')
        arq = open(caminho+nomearquivo+'_'+str(i)+'.txt', 'w')
        
        texto = []
        for j in range(len(vetorvetorX[i])):
            texto.append(str(vetorvetorX[i][j]/60)+'\t'+str(vetorvetorY[i][j])+'\n')
        arq.writelines(texto)
        arq.close()

    

def gerar_gnuplot_script(diretorioGraficos,nomearquivo,vetorArquivos, vetorCores,vetorTitulos,log,titulo):
    diretorioDestino = 'saida_scripts_gnuplot/'
    diretorioGraficos = '/home/lucas/Documents/ns2/graficos/'
    diretorioValores = 'valores_gnuplot/'
    saida = str(diretorioDestino)+str(nomearquivo)+".gp"
    file = open(saida, "w")
    if(log):
        file.write("set log y\n")
    file.write("plot '"+diretorioValores+vetorArquivos[0]+"' with line linecolor '"+vetorCores[0]+"' title '"+vetorTitulos[0]+"'")
    if(len(vetorArquivos) > 1):
        for i in range(len(vetorArquivos)):
            	file.write(", '"+diretorioValores+vetorArquivos[i+1]+"' with line linecolor '"+vetorCores[i+1]+"' title '"+vetorTitulos[i]+"'")
    file.write('\n')
    file.write('set title "'+(titulo)+'"'+'\n')
    file.write("set terminal png size 800,600\n")
    file.write("set output '"+diretorioGraficos+nomearquivo+".png'\n")
    file.write("replot\n")   
    
    file.close()

def gerar_gnuplot_scriptNoTitle(diretorioGraficos,nomearquivo,vetorArquivos, vetorCores,vetorTitulos,log,titulo):
    diretorioDestino = 'saida_scripts_gnuplot/'
    diretorioGraficos = '/home/lucas/Documents/ns2/graficos/'
    diretorioValores = 'valores_gnuplot/'
    saida = str(diretorioDestino)+str(nomearquivo)+".gp"
    file = open(saida, "w")
    if(log):
        file.write("set log y\n")
    file.write("plot '"+diretorioValores+vetorArquivos[0]+"' with line linecolor '"+vetorCores[0]+"' notitle")
    if(len(vetorArquivos) > 1):
        for i in range(len(vetorArquivos)-1):
            	file.write(", '"+diretorioValores+vetorArquivos[i+1]+"' with line linecolor '"+vetorCores[i+1]+"' notitle")
    file.write('\n')
    file.write('set title "'+(titulo)+'"'+'\n')
    file.write("set terminal png size 800,600\n")
    file.write("set output '"+diretorioGraficos+nomearquivo+".png'\n")
    file.write("replot\n")   
    
    file.close()

#pr = subprocess.Popen("gnuplot script_medias.gp", shell = True)
#os.waitpid(pr.pid, 0)


#MATPLOTLIB GRAFICO DE PIZZA
def plota_pizza_matplotLib(labels,valores,cores,explode):
   total = sum(valores)
   plt.pie(valores, explode=explode, labels=labels, colors=cores, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)


arquivo = open(arquivo,"r")

contadorArquivos = 0
vecvecX = []
vecvecY = []

vetorCores = []
vetorTitles = []
vetorArquivos = []

def polo_and_machine(indice):
    #print(indice)
    numPerc = 0
    for i in range(numPolos):
        numPerc += numMaquinasPolo[i]
        if(indice  < numPerc-1):
            return i
    return i

for linha in arquivo:
    numLinhas = 0
    valores = linha.split('\t')
    pontosX = []
    pontosY = []
    #print(valores)
    contador = 0
    saveValue = -1
    for item in valores:
        if(item != '\n'):
            if(float(item) != saveValue):
                saveValue = float(item)
                pontosX.append(saveValue)
                pontosY.append(contadorArquivos+1)
                contador += 1
                if(contador == 2):
                    contador = 0
                    vecvecX.append(pontosX)
                    vecvecY.append(pontosY)
                    print(vecvecY[contadorArquivos][1])
                    pontosX = []
                    pontosY = []
                    print(colorPolos[polo_and_machine(contadorArquivos)])
                    vetorCores.append(colorPolos[polo_and_machine(contadorArquivos)])
                    vetorTitles.append('P'+str(polo_and_machine(contadorArquivos)))
                    vetorArquivos.append(nome+'_'+sobrenome+'_'+seed+'_'+'filescanaisGP_'+str(len(vecvecX))+'.txt')
            else:
                print('aqui houve')
    contadorArquivos += 1

arquivo.close()



'''
contadorFiles = 0
for i in range(numPolos):
    for j in range(numMaquinasPolo[i]):
        vetorCores.append(colorPolos[i])
        vetorTitles.append('P'+str(i)+'M'+str(j))
        print(nome+'_'+seed+'_'+'filescanaisGP_'+str(contadorFiles)+'.txt')
        vetorArquivos.append(nome+'_'+sobrenome+'_'+seed+'_'+'filescanaisGP_'+str(contadorFiles)+'.txt')
        contadorFiles += 1
'''    


gerar_arquivo_leitura_GnuPlot('/home/lucas/Documents/ns2/valores_gnuplot/',nome+'_'+sobrenome+'_'+seed+'_filescanaisGP',vecvecX,vecvecY)
gerar_gnuplot_scriptNoTitle('',nome+'_'+sobrenome+'_'+seed+'_'+'filescanais',vetorArquivos,vetorCores,vetorTitles,False,'Gráfico de duração de envio dos arquivos')
pr = subprocess.Popen("gnuplot saida_scripts_gnuplot/"+nome+'_'+sobrenome+'_'+seed+'_'+"filescanais.gp", shell = True)
os.waitpid(pr.pid, 0)

#GRAFICOS
