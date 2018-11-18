for F in simpleOutput/files/* 
do
	python gerarGraficosGnuPlotFiles.py $F
done

for F in simpleOutput/packets/* 
do
	python gerarGraficosGnuPlotPackets.py $F
done


