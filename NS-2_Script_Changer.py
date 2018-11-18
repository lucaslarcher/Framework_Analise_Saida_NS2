import sys
configFile = open('config.txt', 'r')
configs = []
for line in configFile:
   configs.append(line) 
        
numPolos = int(configs[0].split(' ')[2])
colorPolos = ["red", "blue", "green", "yellow", "black"]
numMachines4Polo = [30,20,47,50,30]
larguraDeBandaPolos = [20,4,4,4,10] #Mb
latenciaPolos = [60,60,60,60,60] #ms
larguraDeBandaServer = 100 #Mb
latenciaServer = 60 #ms
noteTime = 10*60*60
endWork = 2*60*60
timeToSendAfterEndWork = 60*30

def getPoloAndNumber(index):#with a order index, return polo and machine number
    poloAndMachine = []
    sumPolo = 0
    indexPolo = 0
    for machines4Polo in numMachines4Polo:
        sumPolo += machines4Polo
        if(sumPolo > index):
            poloAndMachine.append(indexPolo+1)
            poloAndMachine.append(index - (sumPolo - machines4Polo)+1)
            return poloAndMachine
        indexPolo += 1
            


parametros = []
for param in sys.argv :
    parametros.append(param)
    
fileScript = ''
fileValues = ''
if(len(parametros) != 1):
    fileScript = parametros[1]
    fileValues = parametros[2]


fileValues = open(fileValues, 'r')
indiceLinha = 0

index = 0

fileLostXMin = []

for line in fileValues:
    begin = float(line.split('\t')[0])
    end = float(line.split('\t')[1])
    #end before time 2 hours
    if((end - endWork) > 0):
        #end befores te extended time to send
        if(((end - begin) - (endWork - begin)) > timeToSendAfterEndWork):
            infoPoloMachine = getPoloAndNumber(index)
            fileLostXMin.append('ftpP'+str(infoPoloMachine[0])+'M'+str(infoPoloMachine[1])+'ToServer')
            print(fileLostXMin[len(fileLostXMin)-1])
    index += 1

sumMachines = 0
for machines4Polo in numMachines4Polo:
        sumMachines += machines4Polo
print('Lost files: '+str(len(fileLostXMin))+'/'+str(sumMachines))


print(configs)