from constants import *
from packetStructure import *

#takes takes 50,000 examples and puts it in necessary format for training
csvfiles = [x[:-5] for x in FILENAMES]

for filename in csvfiles:
	print filename
	inputfile = open(filename+'.flow.csv')
	outfile = open(filename+'.features.csv','w')
	line = inputfile.readline().strip()
	while line!='':
		fields = line.split(',')
		#if float(fields[4])!=0 and float(fields[3])!=0 and float(fields[7])!=0:
		outfile.write(
			fields[2] + ',' +
			fields[3] + ',' +
			fields[6] + ',' +
			fields[7] + ',' +
			fields[8] + ',' +
			fields[9] + ',' +
			fields[10] + ',' +
			fields[11] + ',' +
			fields[13] + ',' +
			fields[14] + ',' +
			fields[15] + ',' +
			'\n')
		line = inputfile.readline().strip()
	inputfile.close()
	outfile.close()
