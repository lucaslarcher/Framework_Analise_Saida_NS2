numPolos = 5
colorPolos = ["Red", "Blue", "Green", "Yellow", "Black"]
numMaquinasPolo = [30,20,47,50,30]
larguraDeBandaPolosDownload = [20,4,4,4,10] #Mb
larguraDeBandaPolosUpload = [20,4,4,4,10] #Mb
latenciaPolos = [50,60,55,60,55] #ms
velocidadeUpload = [0.1,0.1,0.1,0.1,0.1] #com relacao ao download
larguraDeBandaServer = 100 #Mb
latenciaServer = 60 #ms
observationTime = 10*60*60
timework = 20*60*60

path = "/home/lucas//Documents/paper_experimento/Framework_Analise_Saida_NS2/scripts/"

import random

typeSendData = 0 #0 - standart (machine-server), 2 after machine-localserver-server
nametypeSendData = ['normal','instantly','after']
subname = nametypeSendData[typeSendData]
typeUpload = 0 #0 - 10%, 1 - 10% to 100%, 2 - 100%, 3 - 46%
nameTypeUpload = ['upload10','upload10to100','upload100','upload46']
nameUpload = nameTypeUpload[typeUpload]
seeds = ["7638544921", "0416802013", "0856592017"]
numSeeds = len(seeds)



for seed in seeds:

    filename = path+subname+nameUpload+'_scriptNS2_'+seed
    arq = open(filename+'.txt', 'w')
    
    outputPath = "/home/lucas//Documents/paper_experimento/Framework_Analise_Saida_NS2/nsOutput/"
    outputFilename = outputPath+subname+nameUpload+'_scriptNS2_'+seed

    random.seed(seed)


    def funcProbabilidadeUpload(larguraDeBanda):
        val = random.random()
        if(typeUpload == 0):
            return larguraDeBanda*random.choice([0.1])#same number of randons for comparation
        if(typeUpload == 1):
            if(val > 0.25):
                return larguraDeBanda*random.uniform(0.1,0.5)
            else:
                return larguraDeBanda*random.uniform(0.6,1)
        if(typeUpload == 2):
            return larguraDeBanda*random.choice([1])#same number of randons for comparation
        if(typeUpload == 3):
            return larguraDeBanda*random.choice([0.46])#same number of randons for comparation



    def funcProbabilidadeEnvio():
        val = random.random()
        if(val > 0.25):
            return random.uniform(115,120)
        else:
            return random.uniform(110,114)
        
    def userActions():

        #Num Acess Moodle
        accessMoodle = 1

        #Num Files
        getFiles = random.randint(1, 3) # 1-5
        sendFile = 1

        #Size
        sizeOfAccessMoodle = random.uniform(1, 3) #1-5

        requests = []

        #Times

        #Moodle access on begin
        for i in range(accessMoodle):
            requests.append([random.uniform(0, 15), sizeOfAccessMoodle, False])
        #Request Files
        for i in range(getFiles):
            requests.append([random.uniform(0, 15), random.uniform(1, 3), False])
        #Send Files
        for i in range(sendFile):
            requests.append([funcProbabilidadeEnvio(), random.uniform(1, 8), True])
    
        
        return requests

    arq.write("#Create a simulator object"+'\n')
    arq.write("set ns [new Simulator]"+'\n')

    arq.write("\n")
    arq.write("#Define different colors for data flows (for NAM)"+'\n')
    for indicePolo in range(numPolos):
        arq.write("$ns color "+str(indicePolo+1)+" "+colorPolos[indicePolo]+'\n')
    arq.write("\n")

    arq.write("#Open the NAM trace file"+'\n')
    arq.write("set nf [open "+outputFilename+".nam w]"+'\n')
    arq.write("$ns namtrace-all $nf"+'\n')

    arq.write("\n")
    arq.write("#Define a 'finish' procedure"+'\n')
    arq.write("proc finish {} {"+'\n')
    arq.write("\t"+"global ns nf"+'\n')
    arq.write("\t" + "$ns flush-trace"+'\n')
    arq.write("\t" + "#Close the NAM trace file"+'\n')
    arq.write("\t" + "close $nf"+'\n')
   # arq.write("\t" + "#Execute NAM on the trace file"+'\n')
  #  arq.write("\t" + "exec nam out.nam &"+'\n')
    arq.write("\t" + "exit 0"+'\n')
    arq.write("}"+'\n')
    arq.write("\n")

    arq.write("#Server Moodle"+'\n')
    arq.write("set internet [$ns node]"+'\n')
    arq.write("set server [$ns node]"+'\n')
    arq.write("$ns duplex-link $internet $server "+str(larguraDeBandaServer)+"Mb "+str(latenciaServer)+"ms DropTail"+'\n')
    arq.write("\n")

    for indicePolo in range(numPolos):
        
        arq.write("#Create nodes Polo "+str(indicePolo+1)+'\n')
        arq.write("set S" + str(indicePolo + 1) + " [$ns node]"+'\n')
        arq.write("$ns simplex-link $internet $S" + str(indicePolo + 1) + " "+str(larguraDeBandaPolosDownload[indicePolo])+"Mb "+str(latenciaPolos[indicePolo])+"ms DropTail"+'\n')
        arq.write("$ns simplex-link $S" + str(indicePolo + 1) + " $internet "+str(funcProbabilidadeUpload(larguraDeBandaPolosDownload[indicePolo]))+"Mb "+str(latenciaPolos[indicePolo])+"ms DropTail"+'\n')

    for indicePolo in range(numPolos):
        #create machine polos
        for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
            arq.write("set P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [$ns node]"+'\n')
       
        
        if(typeSendData == 0):
            arq.write("#Create links between the nodes Polo "+str(indicePolo+1)+'\n')
            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                arq.write("$ns duplex-link $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $S"+ str(indicePolo + 1) + " 100Mb 10ms DropTail"+'\n')
                
        arq.write("\n")
    
    if(typeSendData > 0):
        for indicePolo in range(numPolos):
            arq.write("#Create nodes local server Polo "+str(indicePolo+1)+'\n')
            arq.write("set P" + str(indicePolo + 1) + "LS [$ns node]"+'\n')
            arq.write("$ns duplex-link $S"+str(indicePolo+1)+" $P"+ str(indicePolo + 1) + "LS 100Mb 10ms DropTail"+'\n')

            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                arq.write("$ns duplex-link $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $P"+ str(indicePolo + 1) + "LS 100Mb 10ms DropTail"+'\n')
            

    #Configurando conexao TCP/FTP
    
    for indicePolo in range(numPolos):
        arq.write("\n")
        arq.write("#Create connection TCP Polo "+str(indicePolo+1)+'\n')
        arq.write("\n")
        for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
            #Machine to server
            arq.write("\n")
            arq.write("#Polo "+str(indicePolo+1)+" Maquina "+str(indiceMaquinas+1)+" -- Servidor"+'\n')
            arq.write("set tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer [new Agent/TCP]"+'\n')
            arq.write("$tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer set class_ "+str(indicePolo+1)+'\n')
            arq.write("$ns attach-agent $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer"+'\n')
            arq.write("set sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer [new Agent/TCPSink]"+'\n')
            arq.write("$ns attach-agent $server $sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer"+'\n')
            arq.write("$ns connect $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer $sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer"+'\n')
            arq.write("$tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer set fid_ "+str(indicePolo+1)+'\n')
    
            arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
            arq.write("set ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer [new Application/FTP]"+'\n')
            arq.write("$ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer attach-agent $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer"+'\n')
            arq.write("$ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToServer set type_ FTP"+'\n')
    
            #Server to Machine
            arq.write("#Server -- Polo " + str(indicePolo + 1) + " Maquina " + str(indiceMaquinas + 1)+'\n')
            arq.write("set tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Agent/TCP]"+'\n')
            arq.write("$tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set class_ "+str(indicePolo+1)+'\n')
            arq.write("$ns attach-agent $server $tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
            arq.write("set sinkServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Agent/TCPSink]"+'\n')
            arq.write("$ns attach-agent $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $sinkServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
            arq.write("$ns connect $tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $sinkServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
            arq.write("$tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set fid_ "+str(indicePolo+1)+'\n')
    
            arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
            arq.write("set ftpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Application/FTP]"+'\n')
            arq.write("$ftpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" attach-agent $tcpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
            arq.write("$ftpServerToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set type_ FTP"+'\n')
    
    if(typeSendData == 2):
        for indicePolo in range(numPolos):
            arq.write("\n")
            arq.write("#Create connection TCP Polo "+str(indicePolo+1)+'\n')
            arq.write("\n")
            
            arq.write("#Polo "+str(indicePolo+1)+" Local Server -- Servidor"+'\n')
            arq.write("set tcpServerToLS"+str(indicePolo+1)+" [new Agent/TCP]"+'\n')
            arq.write("$tcpServerToLS"+str(indicePolo+1)+" set class_ "+str(indicePolo+1)+'\n')
            arq.write("$ns attach-agent $server $tcpServerToLS"+str(indicePolo+1)+'\n')
            arq.write("set sinkServerToLS"+str(indicePolo+1)+" [new Agent/TCPSink]"+'\n')
            arq.write("$ns attach-agent $P"+str(indicePolo+1)+"LS $sinkServerToLS"+str(indicePolo+1)+'\n')
            arq.write("$ns connect $tcpServerToLS"+str(indicePolo+1)+" $sinkServerToLS"+str(indicePolo+1)+'\n')
            arq.write("$tcpServerToLS"+str(indicePolo+1)+" set fid_ "+str(indicePolo+1)+'\n')
    
            arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
            arq.write("set ftpServerToLS"+str(indicePolo+1)+" [new Application/FTP]"+'\n')
            arq.write("$ftpServerToLS"+str(indicePolo+1)+" attach-agent $tcpServerToLS"+str(indicePolo+1)+'\n')
            arq.write("$ftpServerToLS"+str(indicePolo+1)+" set type_ FTP"+'\n')
    
            #Server to Machine
            arq.write("#Server -- Polo local server " + str(indicePolo + 1)+'\n')
            arq.write("set tcpLS"+str(indicePolo+1)+"ToServer [new Agent/TCP]"+'\n')
            arq.write("$tcpLS"+str(indicePolo+1)+"ToServer set class_ "+str(indicePolo+1)+'\n')
            arq.write("$ns attach-agent $P"+str(indicePolo+1)+"LS $tcpLS"+str(indicePolo+1)+"ToServer"+'\n')
            arq.write("set sinkLS"+str(indicePolo+1)+"ToServer [new Agent/TCPSink]"+'\n')
            arq.write("$ns attach-agent $server $sinkLS"+str(indicePolo+1)+"ToServer"+'\n')
            arq.write("$ns connect $tcpLS"+str(indicePolo+1)+"ToServer $sinkLS"+str(indicePolo+1)+"ToServer"+'\n')
            arq.write("$tcpLS"+str(indicePolo+1)+"ToServer set fid_ "+str(indicePolo+1)+'\n')
    
            arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
            arq.write("set ftpLS"+str(indicePolo+1)+"ToServer [new Application/FTP]"+'\n')
            arq.write("$ftpLS"+str(indicePolo+1)+"ToServer attach-agent $tcpLS"+str(indicePolo+1)+"ToServer"+'\n')
            arq.write("$ftpLS"+str(indicePolo+1)+"ToServer set type_ FTP"+'\n')
            
            arq.write("\n")
            
            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                #Machine to local server
                arq.write("\n")
                arq.write("#Polo "+str(indicePolo+1)+" Maquina "+str(indiceMaquinas+1)+" -- Local Server"+'\n')
                arq.write("set tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" [new Agent/TCP]"+'\n')
                arq.write("$tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" set class_ "+str(indicePolo+1)+'\n')
                arq.write("$ns attach-agent $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+'\n')
                arq.write("set sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" [new Agent/TCPSink]"+'\n')
                arq.write("$ns attach-agent $P"+str(indicePolo+1)+"LS $sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+'\n')
                arq.write("$ns connect $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" $sinkP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+'\n')
                arq.write("$tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" set fid_ "+str(indicePolo+1)+'\n')
    
                arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
                arq.write("set ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" [new Application/FTP]"+'\n')
                arq.write("$ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" attach-agent $tcpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+'\n')
                arq.write("$ftpP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+"ToLS"+str(indicePolo+1)+" set type_ FTP"+'\n')
    
                #Server to Machine
                arq.write("#Server -- Polo " + str(indicePolo + 1) + " Maquina " + str(indiceMaquinas + 1)+'\n')
                arq.write("set tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Agent/TCP]"+'\n')
                arq.write("$tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set class_ "+str(indicePolo+1)+'\n')
                arq.write("$ns attach-agent $P"+str(indicePolo+1)+"LS $tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
                arq.write("set sinkLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Agent/TCPSink]"+'\n')
                arq.write("$ns attach-agent $P"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $sinkLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
                arq.write("$ns connect $tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" $sinkLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
                arq.write("$tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set fid_ "+str(indicePolo+1)+'\n')
    
                arq.write("#Configurando uma aplicacao FTP para o TCP"+'\n')
                arq.write("set ftpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" [new Application/FTP]"+'\n')
                arq.write("$ftpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" attach-agent $tcpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'\n')
                arq.write("$ftpLS"+str(indicePolo+1)+"ToP"+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+" set type_ FTP"+'\n')

    if(typeSendData == 0):
        #Tasks normal
        for indicePolo in range(numPolos):
            arq.write("\n")
            arq.write("#Create Task TCP Polo "+str(indicePolo+1)+'\n')
            arq.write("\n")
            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                userRequets = userActions()
                for request in userRequets:
                    if(request[2]):
                        arq.write("$ns at "+str(request[0] * 60)+' "$ftpP'+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'ToServer send '+str(request[1]*1024*1024)+'"'+'\n')
                    else:
                        arq.write("$ns at "+str(request[0] * 60) + ' "$ftpServerToP'+str(indicePolo + 1) + "M" + str(indiceMaquinas + 1) + ' send ' + str(request[1]*1024*1024) + '"'+'\n')
    
   
    if(typeSendData == 1):
        #Tasks enviando de apenas uma maquina imediatamente
        for indicePolo in range(numPolos):
            arq.write("\n")
            arq.write("#Create Task TCP Polo "+str(indicePolo+1)+'\n')
            arq.write("\n")
            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                userRequets = userActions()
                for request in userRequets:
                    if(request[2]):
                        arq.write("$ns at "+str(request[0] * 60)+' "$ftpP'+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'ToServer send '+str(request[1]*1024*1024)+'"'+'\n')
                    else:
                        arq.write("$ns at "+str(request[0] * 60) + ' "$ftpServerToP'+str(indicePolo + 1) + "M" + str(indiceMaquinas + 1) + ' send ' + str(request[1]*1024*1024) + '"'+'\n')

    if(typeSendData == 2):
         #Tasks enviando de apenas uma ao final
         for indicePolo in range(numPolos):
            arq.write("\n")
            arq.write("#Create Task TCP Polo "+str(indicePolo+1)+'\n')
            arq.write("\n")
            for indiceMaquinas in range(numMaquinasPolo[indicePolo]):
                userRequets = userActions()
                for request in userRequets:
                    if(request[2]):
                        arq.write("$ns at "+str(request[0] * 60)+' "$ftpP'+str(indicePolo+1)+"M"+str(indiceMaquinas+1)+'ToLS'+str(indicePolo+1)+' send '+str(request[1]*1024*1024)+'"'+'\n')
                        arq.write("$ns at "+str(2* 60 * 60)+' "$ftpLS'+str(indicePolo+1)+'ToServer send '+str(request[1]*1024*1024)+'"'+'\n')
                    else:
                        arq.write("$ns at "+str(request[0] * 60) + ' "$ftpServerToP'+str(indicePolo + 1) + "M" + str(indiceMaquinas + 1) + ' send ' + str(request[1]*1024*1024) + '"'+'\n')

    arq.write("\n")
    
    #Chama o metdo finish aos 5 s
    arq.write("$ns at "+str(observationTime)+' "finish"')
    arq.write("\n")

    arq.write("#Run the simulation"+'\n')
    arq.write("$ns run"+'\n')

    arq.close


