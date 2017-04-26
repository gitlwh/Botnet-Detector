from constants import *
import multiprocessing as MP
import subprocess

def executeCommand(command,outfilename):
	sem.acquire()

	subprocess.call(command, shell = True)
	
	infile = open(outfilename, 'r')
	data = [eachline.strip() for eachline in infile]
	infile.close()
	
	data = preprocess(data)
	
	outfile = open(outfilename+".csv",'w')
	for eachcomponent in data:
		outfile.write(eachcomponent)
	outfile.close()
	
	print 'done processing : ' + outfilename
	sem.release()

def preprocess(data):
	outputdata = []
	for eachline in data:
		fields = eachline.split(',')
		
		#sanity check for 6 fields. Has to be changed if tshark options are changed
		if len(fields) != 6:
			continue

		tcppayload = fields[4].strip()
		udppayload = fields[5].strip()

		#subtract udp header length	
		if udppayload != '':
			fields[5] = str(int(udppayload) - UDP_HEADERLENGTH)
			if int(fields[5]) <= 0:
				continue
		#ignore packet if both tcp and udp payload lengths are null
		elif tcppayload == '' or tcppayload == '0':
			continue

		#add all valid fields to output list
		for eachfield in fields:
			if eachfield.strip() != '':
				outputdata.append(eachfield)
				outputdata.append(',')
		outputdata.pop()
		outputdata.append('\n')
	return outputdata

commands = [[i,parameters] for i in FILENAMES]
print commands
sem = MP.Semaphore(THREADLIMIT)

for command in commands:
	print command[0]
	finalCommand = 'tshark -r ' + command[0] + ' ' + command[1] + ' ' + '>' +command[0][:-5]
	print finalCommand
	task = MP.Process(target = executeCommand, args = (finalCommand, command[0][:-5],))
	task.start()


