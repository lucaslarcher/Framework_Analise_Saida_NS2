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
if(len(parametros) != 1):
    arquivo = parametros[1]
    seed = parametros[1].split('_')
    seed = seed[2].split('.')[0]
    nome = (parametros[1].split('_')[0]+'_'+parametros[1].split('_')[1]).split('/')
    nome = nome[(len(nome)-1)]

numPolos = 5
timeWork = 4*60*60

pathSaida = "/home/lucas/Documents/ns2/graficos/"
subName = nome+"_"+seed+"_"

ack = 0
nack = 0
h = 0
d = 0
r = 0

timeACK = []
timeNACK = []
timeH = []
timeD = []
timeR = []
    
#each server
timeServer = []
for i in range(5*2):#one for each server source and destine
    time = []
    timeServer.append(time)
    
#para cada polo
timePolos = []
for i in range(numPolos):#one for each polo
    polo = []
    for i in range(5*2):#ack,nack,h,d,r source and destine
        time = []
        polo.append(time)
    timePolos.append(polo)
#timerpolos[indice polo][indice do tipo][indice do tempo em segundos]

linhasDesinteressantes = []
linhasDesinteressantes.append(0)
linhasDesinteressantes.append(1)

linhasServer =  2*5
linhasPolos = 2*5*numPolos



arquivo = open(arquivo,"r")


for i in range(3):#linhas inuteis
    arquivo.readline()    
    
linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
ack = int(valores[0])
nack = int(valores[1])
h = int(valores[2])
d = int(valores[3])
r = int(valores[4])

linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
for valor in valores:
    timeACK.append(int(valor))
linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
for valor in valores:
    timeNACK.append(int(valor))
linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
for valor in valores:
    timeH.append(int(valor))
linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
for valor in valores:
    timeD.append(int(valor))
linha = arquivo.readline()
valores = linha[1:len(linha)-2].split(',')
for valor in valores:
    timeR.append(int(valor))

for i in range(2):#linhas inuteis
    arquivo.readline()   

for i in range(linhasServer):
    linha = arquivo.readline()
    valores = linha[1:len(linha)-2].split(',')
    for valor in valores:
        timeServer[i].append(int(valor))

for i in range(4):#linhas inuteis
    arquivo.readline()   
    
for p in range(numPolos):
    for i in range(2*5):
        linha = arquivo.readline()
        valores = linha[1:len(linha)-2].split(',')
        for valor in valores:
            timePolos[p][i].append(int(valor))
    
    for i in range(2):#linhas inuteis
        arquivo.readline()   
    
arquivo.close()

import os
import subprocess

#FUNCOES DE GERACAO DE GRAFICOS

def gerar_arquivo_leitura_GnuPlot(caminho,nomearquivo,vetorvetorX,vetorvetorY):
    
    for i in range(len(vetorvetorX)):
        arq = open(caminho+nomearquivo+'_'+str(i)+'.txt', 'w')
        texto = []
        for j in range(len(vetorvetorX[i])):
            texto.append(str(vetorvetorX[i][j])+'\t'+str(vetorvetorY[i][j])+'\n')
        arq.writelines(texto)
        arq.close()

    
def gerar_arquivo_leitura_GnuPlot_Por_Minuto(caminho,nomearquivo,vetorvetorX,vetorvetorY):
    
    for i in range(len(vetorvetorX)):
        arq = open(caminho+nomearquivo+'_'+str(i)+'.txt', 'w')
        texto = []
        contador = 0
        x = 0
        y = 0
        for j in range(len(vetorvetorX[i])):
            y += vetorvetorY[i][j]
            if(contador == 60):
                texto.append(str(x)+'\t'+str(y)+'\n')
                y = 0
                x += 1
                contador = -1
            contador += 1
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
        for i in range(len(vetorArquivos)-1):
            	file.write(", '"+diretorioValores+vetorArquivos[i+1]+"' with line linecolor '"+vetorCores[i+1]+"' title '"+vetorTitulos[i+1]+"'")
    file.write('\n')
    file.write('set title "'+(titulo)+'"'+'\n')
    file.write("set terminal png size 800,600\n")
    file.write("set output '"+diretorioGraficos+nomearquivo+".png'\n")
    file.write("replot\n")   
    
    file.close()

#pr = subprocess.Popen("gnuplot script_medias.gp", shell = True)
#os.waitpid(pr.pid, 0)


def gerar_barras_gnuplot_script(diretorioGraficos,nomearquivo,vetorArquivos, vetorCores,vetorTitulos,log):
    diretorioDestino = 'saida_scripts_gnuplot/'
    diretorioGraficos = '/home/lucas/Documents/ns2/graficos/'
    diretorioValores = 'valores_gnuplot/'
    saida = str(diretorioDestino)+str(nomearquivo)+".gp"
    file = open(saida, "w")
    if(log):
        file.write("set log y\n")
    file.write("plot '"+diretorioValores+vetorArquivos[0]+"' with boxes lc '"+vetorCores[0]+"' title '"+vetorTitulos[0]+"'")
    if(len(vetorArquivos) > 1):
        for i in range(len(vetorArquivos)-1):
            	file.write(", '"+diretorioValores+vetorArquivos[i+1]+"' with boxes lc '"+vetorCores[i+1]+"' title '"+vetorTitulos[i+1]+"'")
    file.write('\n')
    file.write("set terminal png size 800,600\n")
    file.write("set output '"+diretorioGraficos+nomearquivo+"_boxes.png'\n")
    file.write("replot\n")
    

#MATPLOTLIB GRAFICO DE PIZZA
def plota_pizza_matplotLib(labels,valores,cores,explode):
   total = sum(valores)
   plt.pie(valores, explode=explode, labels=labels, colors=cores, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)


valdpi = 200
vecSecs = []
for i in range(timeWork):
    vecSecs.append(i)


vectorvectorX = []
vectorvectorY = []
vectorvectorX.append(vecSecs)
vectorvectorX.append(vecSecs)
vectorvectorY.append(timeD)
envios = []
for i in range(len(timeACK)):
    envios.append(0)
    envios[i] = timeACK[i]
    envios[i] += timeNACK[i]
    envios[i] += timeH[i]
    envios[i] += timeR[i]
vectorvectorY.append(envios)

vetorArquivos = []
for i in range(2):
    vetorArquivos.append(nome+'_'+seed+'_'+'globalGP_'+str(i)+'.txt')

vetorCores = []
vetorCores.append('red')
vetorCores.append('blue')
vetorCores.append('green')
vetorCores.append('yellow')
vetorCores.append('orange')
vetorCores.append('purple')
vetorCores.append('violet')

vetorTitles = []
vetorTitles.append('Drop')
vetorTitles.append('Envios')

gerar_arquivo_leitura_GnuPlot_Por_Minuto('/home/lucas/Documents/ns2/valores_gnuplot/',nome+'_'+seed+'_globalGP',vectorvectorX,vectorvectorY)
gerar_gnuplot_script('',nome+'_'+seed+'_'+'global',vetorArquivos,vetorCores,vetorTitles,True,'Gráfico de envios e perdas globais')
pr = subprocess.Popen("gnuplot saida_scripts_gnuplot/"+nome+'_'+seed+'_'+"global.gp", shell = True)
os.waitpid(pr.pid, 0)

enviosInicio = 0
enviosFinal = 0
dropsInicio = 0
dropsFinal = 0
for i in range(60*60):
    enviosInicio+=envios[i]
    dropsInicio+=timeD[i]
for i in range(60*60+1,60*60*3):
    enviosFinal+=envios[i]
    dropsFinal+=timeD[i]    
    
cor1='blue'
cor2='green'
label1='Envios'
label2='Drops'

vetor1 = []
vetor2 = []
vetor1.append(enviosInicio)
vetor1.append(dropsInicio)
vetor2.append(enviosFinal)
vetor2.append(dropsFinal)
print(vetor1)
print(vetor2)

data = []
data.append(vetor1)
data.append(vetor2)

dim = len(data[0])
w = 0.75
dimw = w / dim

fig, ax = plt.subplots()
x = np.arange(len(data))
for i in range(len(data[0])):
    y = [d[i] for d in data]
    b = ax.bar(x + i * dimw, y, dimw, bottom=0.001)

ax.set_xticks(x + dimw / 2)
ax.set_yscale('log')

ax.set_xlabel('Período')
ax.set_ylabel('Pacotes')
ax.set_xticklabels(('Período inicial (Downloads)','Período final (Uploads)'))
plt.legend(('Envios','Drops'))
plt.title('Envios e Drops nos períodos críticos') 
#plt.show()
plt.savefig('/home/lucas/Documents/ns2/graficos/'+nome+'_'+seed+'_canais_enviosedrops_barras.png') 

plt.clf()

vectorvectorX = []
vectorvectorY = []
vetorTitles = []
vetorArquivos = []
for i in range(1+numPolos):
    vetorArquivos.append(nome+'_'+seed+'_'+'canaisGP_'+str(i)+'.txt')

dropServer = []
for i  in range(len(timeServer[3])):
    dropServer.append(timeServer[3][i]+timeServer[8][i])

vectorvectorY.append(dropServer)
vectorvectorX.append(vecSecs)
vetorTitles.append('Server')


for i  in range(numPolos):
    dropPolo = []
    for j  in range(len(timePolos[i][3])):
        dropPolo.append(timePolos[i][3][j]+timePolos[i][8][j])
    vectorvectorY.append(dropPolo)
    vectorvectorX.append(vecSecs)
    vetorTitles.append('Polo '+str(i+1))
    
gerar_arquivo_leitura_GnuPlot_Por_Minuto('/home/lucas/Documents/ns2/valores_gnuplot/',nome+'_'+seed+'_canaisGP',vectorvectorX,vectorvectorY)
gerar_gnuplot_script('',nome+'_'+seed+'_'+'canais',vetorArquivos,vetorCores,vetorTitles,False,'Gráfico de perdas por cada ponto de interesse')
pr = subprocess.Popen("gnuplot saida_scripts_gnuplot/"+nome+'_'+seed+"_canais.gp", shell = True)
os.waitpid(pr.pid, 0)

vectorDropsTotaisIniciais = []
vectorDropsTotaisFinais = []
#Para o servidor
contador = 0
for i in range(60*60):
    contador += vectorvectorY[0][i]
vectorDropsTotaisIniciais.append(contador)
contador = 0
for i in range(60*60+1,60*60*3):
    contador += vectorvectorY[0][i]
vectorDropsTotaisFinais.append(contador)

for j  in range(1,numPolos+1):
    contador = 0
    for i in range(60*60):
        contador += vectorvectorY[j][i]
    vectorDropsTotaisIniciais.append(contador)
    contador = 0
    for i in range(60*60+1,60*60*3):
        contador += vectorvectorY[j][i]
    vectorDropsTotaisFinais.append(contador)

#MATPLOTLIB GRAFICO DE PIZZA


def plot_pizza(labels,valores,cores):
   iteradorErrosPos = 0 
   iteradorErrosNeg = 0 
   total = sum(valores)
   porcents = ["{:.2f}%".format((x/total)*100) for x in valores]
   #plt.pie(valores, explode=explode, labels=labels, colors=cores, autopct=lambda p: '{:.0f}'.format(p * total / 100), shadow=True, startangle=90)
   wedges, texts = plt.pie(valores, colors=cores, shadow=True, startangle=90)
   bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
   kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
   for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    xtext = 1.35*np.sign(x)
    ytext =  1.4*y
    if((valores[i]/total)*100 < 10):
        if(x<0):
            xtext +=  .3*iteradorErrosNeg
            ytext -= .02 + .15*iteradorErrosNeg
            iteradorErrosNeg+=1
        else:
            xtext -= .4*iteradorErrosPos 
            ytext -= .02 + .15*iteradorErrosPos
            iteradorErrosPos+=1
        
        
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    plt.annotate(porcents[i], xy=(x, y), xytext=(xtext,ytext), horizontalalignment=horizontalalignment, **kw) 
   

#Grafico de pizza para porcentagem de drops e envios
plt.clf()

labels = []
labels.append('Envios')
labels.append('Drops')
valores = []
valores.append(ack+nack+r+h)
valores.append(d)
cores = vetorCores

plot_pizza(labels,valores,cores)
plt.gca().legend(labels,loc='center',bbox_to_anchor=(-.04,.04))
plt.axis('equal') 
#plt.show()
#plt.title('Perdas de pacotes ao final do processo (Uploads)') 
plt.savefig('/home/lucas/Documents/ns2/graficos/'+nome+'_'+seed+'_dropsenviosGeral__pie.png') 
 
plt.clf()

# Determina que as proporcoes sejam iguais ('equal') de modo a desenhar o circulo
labels = vetorTitles
valores = vectorDropsTotaisIniciais
cores = vetorCores

plot_pizza(labels,valores,cores)
plt.gca().legend(labels,loc='center',bbox_to_anchor=(-.04,.04))
plt.axis('equal') 
#plt.show()
#plt.title('Perdas de pacotes ao início do processo (Downloads)') 
plt.savefig('/home/lucas/Documents/ns2/graficos/'+nome+'_'+seed+'_canais_dropsiniciais__pie.png') 

plt.clf()
# Determina que as proporcoes sejam iguais ('equal') de modo a desenhar o circulo
labels = vetorTitles
valores = vectorDropsTotaisFinais
cores = vetorCores

plot_pizza(labels,valores,cores)
plt.gca().legend(labels,loc='center',bbox_to_anchor=(-.04,.04))
plt.axis('equal') 
#plt.show()
#plt.title('Perdas de pacotes ao final do processo (Uploads)') 
plt.savefig('/home/lucas/Documents/ns2/graficos/'+nome+'_'+seed+'_canais_dropsfinais__pie.png') 
 
#Grafico de pizza para porcentagem de drops e envios
plt.clf()

labels = []
labels.append('Envios')
labels.append('Drops')
valores = []
valores.append(ack+nack+r+h)
valores.append(d)
cores = vetorCores

plot_pizza(labels,valores,cores)
plt.gca().legend(labels,loc='center',bbox_to_anchor=(-.04,.04))
plt.axis('equal') 
#plt.show()
#plt.title('Perdas de pacotes ao final do processo (Uploads)') 
plt.savefig('/home/lucas/Documents/ns2/graficos/'+nome+'_'+seed+'_dropsenviosGeral__pie.png') 
 


#GRAFICOS
