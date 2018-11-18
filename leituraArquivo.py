import sys

parametros = []
for param in sys.argv :
    parametros.append(param)
    

arquivo = ''
seed = ''
name = ''
intervals = None

if(len(parametros) > 1):
    arquivo = parametros[1]
    seed = parametros[1].split('_')
    seed = seed[2].split('.')[0]
    name = (parametros[1].split('_')[0]).split('/')[1]
    if(len(parametros) > 2):
        intervals = parametros[2]
    print(name)

servidor = 1
internet = 1
numPolos = 5
numMaquinasPolo = [30,20,47,50,30]
timeWork = 10*60*60
timeBeginUpload = 100*60
pularlinhas = 0

#quantidade de nos
pularlinhas += servidor + internet + numPolos
for m in numMaquinasPolo:
    pularlinhas += m

#Quantidade de conexoes
pularlinhas += internet + numPolos*2
for m in numMaquinasPolo:
    pularlinhas += m

#Quantidade de cores
pularlinhas += numPolos

#Cabecalho
pularlinhas += 3

print(pularlinhas)



#variaveis de interesse

#Quantidade total de requisicoes
ack = 0
nack = 0
h = 0
d = 0
r = 0
#Quantidadede de tipos de requisicao por segundo
timeACK = []
timeNACK = []
timeH = []
timeD = []
timeR = []
for i in range(timeWork):
    timeACK.append(0)
    timeNACK.append(0)
    timeH.append(0)
    timeD.append(0)
    timeR.append(0)
#total para cada tipo de mensagem

#Quantidadede de tipos de requisicao por segundo para arestas importantes


#para cada polo
timePolos = []
for i in range(numPolos):#one for each polo
    polo = []
    for i in range(5*2):#ack,nack,h,d,r source and destine
        time = []
        for k in range(timeWork):#timework
            time.append(0)
        polo.append(time)
    timePolos.append(polo)
#timerpolos[indice polo][indice do tipo][indice do tempo em segundos]

#each server
timeServer = []
for i in range(5*2):#one for each server source and destine
    time = []
    for k in range(timeWork):#timework
        time.append(0)
    timeServer.append(time)

#timerserver[indice do tipo][indice do tempo em segundos]


#PARA ARQUIVOS (FILES)
numMaquinasTotal = 0
for m in numMaquinasPolo:
    numMaquinasTotal += m
indicePolos = [] #index plo vector
timeBeginFiles = []
timeEndFiles = []
for i in range(numMaquinasTotal):
    indicePolos.append(i+2+5) #polo index
    timeBegin = []
    timeEnd = []
    timeBeginFiles.append(timeBegin)
    timeEndFiles.append(timeEnd)

timeBeginFilesLostIntervals = []
timeEndFilesLostIntervals = []
limitSecondsSendFile = []

if(intervals != None):
    intervals = intervals.split(',')
    for interval in intervals:  
        #create new interval
        limitSecondsSendFile.append(float(interval))
        timeBeginFilesLostInterval = []
        timeEndFilesLostInterval = []
        timeBeginFilesLostIntervals.append(timeBeginFilesLostInterval)
        timeEndFilesLostIntervals.append(timeEndFilesLostInterval)
        
        idxInterval = len(timeBeginFilesLostIntervals) - 1
        
        for i in range(numMaquinasTotal):
            indicePolos.append(i+2+numPolos) #polo index numPols plus num server plus internet node
            timeBegin = []
            timeEnd = []
            timeBeginFilesLostIntervals[idxInterval].append(timeBegin)
            timeEndFilesLostIntervals[idxInterval].append(timeEnd)

#timerpolos[indice polo][indice do tipo][indice do tempo em segundos]

arquivo = open(arquivo, 'r')
indiceLinha = 0

for entrada in arquivo:
    indiceLinha += 1
    info = entrada.split(" ") # spliting line
    #print(info)
    if(info[0] == "+" or info[0] == "-" or info[0] == "h" or info[0] == "r" or info[0] == "d"):#jumping not useful lines
           
        if(float(info[2]) > timeBeginUpload):
            info1 = int(info[18][1:info[18].find('.')])
            info2 = int(info[19][:info[19].find('.')])
            if((info1 > (numPolos + 1) and info1 < (numMaquinasTotal + numPolos + 2))  or (info2 > (numPolos + 1) and info2 < (numMaquinasTotal + numPolos + 2))): # communication about server or machine
                i=-1
                if(info1 > (numPolos + 1) and info1 < (numMaquinasTotal + numPolos + 2)):
                    i = info1 - 2 - numPolos
                else:
                    i = info2 - 2 - numPolos
                if(len(timeEndFiles[i]) == 0):
                    val = float(info[2])
                    timeBeginFiles[i].append(val)
                    timeEndFiles[i].append(val)
                else:
                    timeEndFiles[i][len(timeEndFiles[i])-1] = float(info[2])
                    '''
                    if(int(timeEndFiles[i][len(timeEndFiles[i])-1] - timeBeginFiles[i][len(timeBeginFiles[i])-1]) > limiteSegundosEnvioArquivo):
                        timeBeginFiles[i].append(float(info[2]))
                        timeEndFiles[i].append(float(info[2]))
                    else:
                        timeEndFiles[i][len(timeEndFiles[i])-1] = float(info[2])
                    '''
                    
        if(float(info[2]) > timeBeginUpload): # look after upload time
            if(intervals != None):
                for indexInterval in range(len(intervals)):#for each interval
                    info1 = int(info[18][1:info[18].find('.')])
                    info2 = int(info[19][:info[19].find('.')])
                    if((info1 > (numPolos + 1) and info1 < (numMaquinasTotal + numPolos + 2))  or (info2 > (numPolos + 1) and info2 < (numMaquinasTotal + numPolos + 2))): # communication about server or machine
                        i=-1
                        if(info1 > (numPolos + 1) and info1 < (numMaquinasTotal + numPolos + 2)):
                            i = info1 - 2 - numPolos
                        else:
                            i = info2 - 2 - numPolos

                        if(len(timeBeginFilesLostIntervals[indexInterval][i]) == 0):
                            val = float(info[2])
                            timeBeginFilesLostIntervals[indexInterval][i].append(val)
                            timeEndFilesLostIntervals[indexInterval][i].append(val)
                        else:
                            if((float(info[2]) - timeEndFilesLostIntervals[indexInterval][i][len(timeEndFilesLostIntervals[indexInterval][i])-1]) > limitSecondsSendFile[indexInterval]):
                                val = float(info[2])
                                timeBeginFilesLostIntervals[indexInterval][i].append(val)
                                timeEndFilesLostIntervals[indexInterval][i].append(val)
                            else:
                                timeEndFilesLostIntervals[indexInterval][i][len(timeEndFilesLostIntervals[indexInterval][i])-1] = float(info[2])


        
        if(int(float(info[2])-0.5) < timeWork):#change for integer time imput
        
        #TYPE OF IMPUT + - r h d
            if(info[0] == "+"):
                ack += 1
                timeACK[int(float(info[2])-0.5)] += 1
                if(int(info[6]) == 1 or int(info[4]) == 1):
                    if(int(info[4]) == 1): #source count
                        timeServer[0][int(float(info[2]) - 0.5)] += 1
                    else:
                        timeServer[5][int(float(info[2]) - 0.5)] += 1
                else:#polo count
                    if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1) or (int(info[4]) < numPolos + 2 and int(info[4]) > 1)):
                        if((int(info[6]) < numPolos + 2 and int(info[6]) > 1)):
                            timePolos[int(info[6])-2][5][int(float(info[2]) - 0.5)] += 1#indice do polo, tipo de resposta,tempo
                        else:
                            timePolos[int(info[4])-2][0][int(float(info[2]) - 0.5)] += 1
    
            if(info[0] == "-"):
                nack += 1
                timeNACK[int(float(info[2]) - 0.5)] += 1
                if(int(info[6]) == 1 or int(info[4]) == 1):
                    if(int(info[4]) == 1): #source
                        timeServer[1][int(float(info[2]) - 0.5)] += 1
                    else:
                        timeServer[6][int(float(info[2]) - 0.5)] += 1
                else:
                    if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1) or (int(info[4]) < numPolos + 2 and  int(info[4]) > 1)):
                        if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1)):
                            timePolos[int(info[6])-2][6][int(float(info[2]) - 0.5)] += 1#indice do polo, tipo de resposta,tempo
                        else:
                            timePolos[int(info[4])-2][1][int(float(info[2]) - 0.5)] += 1
    
            if(info[0] == "h"):
                h += 1
                timeH[int(float(info[2]) - 0.5)] += 1
                if(int(info[6]) == 1 or int(info[4]) == 1):
                    if(int(info[4]) == 1): #source
                        timeServer[2][int(float(info[2]) - 0.5)] += 1
                    else:
                        timeServer[7][int(float(info[2]) - 0.5)] += 1
                else:
                    if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1) or (int(info[4]) < numPolos + 2 and  int(info[4]) > 1)):
                        if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1)):
                            timePolos[int(info[6])-2][7][int(float(info[2]) - 0.5)] += 1#indice do polo, tipo de resposta,tempo
                        else:
                            timePolos[int(info[4])-2][2][int(float(info[2]) - 0.5)] += 1
                            
            if(info[0] == "d"):
                d += 1
                timeD[int(float(info[2]) - 0.5)] += 1
                if(int(info[6]) == 1 or int(info[4]) == 1):
                    if(int(info[4]) == 1): #source
                        timeServer[3][int(float(info[2]) - 0.5)] += 1
                    else:
                        timeServer[8][int(float(info[2]) - 0.5)] += 1
                else:
                    if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1) or (int(info[4]) < numPolos + 2 and  int(info[4]) > 1)):
                        #print(d)
                        #print(info)
                        if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1)):
                            timePolos[int(info[6])-2][8][int(float(info[2]) - 0.5)] += 1#indice do polo, tipo de resposta,tempo
                        else:
                            timePolos[int(info[4])-2][3][int(float(info[2]) - 0.5)] += 1
                       
            if(info[0] == "r"):
                r += 1
                timeR[int(float(info[2]) - 0.5)] += 1
                if(int(info[6]) == 1 or int(info[4]) == 1):
                    if(int(info[4]) == 1): #source
                        timeServer[4][int(float(info[2]) - 0.5)] += 1
                    else:
                        timeServer[9][int(float(info[2]) - 0.5)] += 1
                else:
                    if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1) or (int(info[4]) < numPolos + 2 and  int(info[4]) > 1)):
                        if((int(info[6]) < numPolos + 2 and  int(info[6]) > 1)):
                            timePolos[int(info[6])-2][9][int(float(info[2]) - 0.5)] += 1#indice do polo, tipo de resposta,tempo
                        else:
                            timePolos[int(info[4])-2][4][int(float(info[2]) - 0.5)] += 1
                            
                
        

print("ack: "+str(ack))
print("nack: "+str(nack))
print("h: "+str(h))
print("d: "+str(d))
print("r: "+str(r))

arquivo.close()

#saida de processamento
path = "/home/lucas/Documents/ns2/simpleOutput/files/"

#ARQUIVOS FILES
saidaFiles = []

for indice in range(len(timeBeginFiles)):
    if(len(timeBeginFiles[indice]) > 0):
        saidaFiles.append(str(timeBeginFiles[indice][0])+'\t'+str(timeEndFiles[indice][0])+'\n')
    
arq = open(path+name+'_arquivos_'+seed+'.txt', 'w')
arq.writelines(saidaFiles)
arq.close()

print(timeBeginFilesLostIntervals)
print(timeEndFilesLostIntervals)

if(intervals != None):
    for indexInterval in range(len(timeBeginFilesLostIntervals)):#for each interval
        saidaFiles = []
        for indice in range(len(timeBeginFilesLostIntervals[indexInterval])):
            if(len(timeBeginFilesLostIntervals[indexInterval][indice]) > 0):
                saida = ''
                for jindice in range(len(timeBeginFilesLostIntervals[indexInterval][indice])):
                    saida = saida + str(timeBeginFilesLostIntervals[indexInterval][indice][jindice])+'\t'+str(timeEndFilesLostIntervals[indexInterval][indice][jindice])+'\t'
                saidaFiles.append(saida+'\n')
        arq = open(path+name+'_arquivosLost'+intervals[indexInterval]+'_'+seed+'.txt', 'w')
        arq.writelines(saidaFiles)
        arq.close()


#PACOTES PACKETS
path = "/home/lucas/Documents/ns2/simpleOutput/packets/"
arq = open(path+name+'_dados_'+seed+'.txt', 'w')
texto = []

texto.append("\n%numeros totais ACK, NACK, H D, R"+'\n')
texto.append("\n["+str(ack)+","+str(nack)+","+str(h)+","+str(d)+","+str(r)+"]"+'\n')
texto.append(str(timeACK)+'\n')
texto.append(str(timeNACK)+'\n')
texto.append(str(timeH)+'\n')
texto.append(str(timeD)+'\n')
texto.append(str(timeR)+'\n')


texto.append("\n%numeros servidor source[ACK, NACK, H D, R] destine[ACK, NACK, H D, R]"+'\n')
texto.append(str(timeServer[0])+'\n')
texto.append(str(timeServer[1])+'\n')
texto.append(str(timeServer[2])+'\n')
texto.append(str(timeServer[3])+'\n')
texto.append(str(timeServer[4])+'\n')
texto.append(str(timeServer[5])+'\n')
texto.append(str(timeServer[6])+'\n')
texto.append(str(timeServer[7])+'\n')
texto.append(str(timeServer[8])+'\n')
texto.append(str(timeServer[9])+'\n')

texto.append("\n%numeros de polos source[ACK, NACK, H D, R] destine[ACK, NACK, H D, R]"+'\n')    
texto.append(str(numPolos)+'\n')    

for i in range(numPolos):
    texto.append("#Polo:"+str(i)+'\n')
    texto.append(str(timePolos[i][0])+'\n')
    texto.append(str(timePolos[i][1])+'\n')
    texto.append(str(timePolos[i][2])+'\n')
    texto.append(str(timePolos[i][3])+'\n')
    texto.append(str(timePolos[i][4])+'\n')
    texto.append(str(timePolos[i][5])+'\n')
    texto.append(str(timePolos[i][6])+'\n')
    texto.append(str(timePolos[i][7])+'\n')
    texto.append(str(timePolos[i][8])+'\n')
    texto.append(str(timePolos[i][9])+'\n'+'\n')
    
arq.writelines(texto)
arq.close()

#FILES SENDED


