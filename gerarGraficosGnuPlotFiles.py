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
    numPerc = 0
    for i in range(numPolos):
        numPerc += numMaquinasPolo[i]
        if(indice  < numPerc):
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
                    pontosX = []
                    pontosY = []
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
'''

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
 

'''
#GRAFICOS
