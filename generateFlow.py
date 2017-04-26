from constants import *
from packetStructure import *
import multiprocessing as MP
import subprocess

def packetsToFlows(packets,timegap):
	#sanity check for 0 packets 
	if len(packets) == 0:
		return None

	outputflows = []
	
	#perform a radix-sort to group together packets
	#with same ip-pairs(packet.key represents an ip-pair) 
	#and sort these packets according to timestamp
	packets.sort(key = lambda packet:packet.timestamp)
	packets.sort(key = lambda packet:packet.key)
	
	nextflow = Flow(None)
	for nextpacket in packets:
		#if ip-pairs dont match or time-difference of prev and current packet greater
		#than timegap, create a new flow 
		if (nextflow.key != nextpacket.key) or ((nextpacket.timestamp - nextflow.getEnd()) > timegap):
			nextflow = Flow(nextpacket)
			outputflows.append(nextflow)
		#if not then add packet to previous flow
		else:
			nextflow.addPacket(nextpacket)

	return outputflows

#write list of flows into file in desired format
def writeFlowsToFile(flowlist, filename):
	outfile = open(filename, 'w')
	for flow in flowlist:
		#print "a"
		'''
		print socket.inet_ntoa(flow.ip1) + ',' +\
			socket.inet_ntoa(flow.ip2) + ',' +\
			str(flow.n_packet1) + ',' +\
			str(sum(flow.n_byte1)) + ',' +\
			'%.6f'%flow.t_start1 + ',' +\
			'%.6f'%flow.t_end1 + ',' +\
			'%.6f'%flow.getInterArrivaltime1() + ',' + \
			'%.6f'%flow.getVarOfBytes1() + ',' +\
			'%.6f'%flow.getInterArrivalvar1() + ','
		'''
		outfile.write(
			socket.inet_ntoa(flow.ip1) + ',' +
			socket.inet_ntoa(flow.ip2) + ',' +
			str(flow.n_packet1) + ',' +
			str(sum(flow.n_byte1)) + ',' +
			'%.6f'%flow.t_start1 + ',' +
			'%.6f'%flow.t_end1 + ',' +
			'%.6f'%flow.getInterArrivaltime1() + ',' + 
			'%.6f'%flow.getVarOfBytes1() + ',' +
			'%.6f'%flow.getInterArrivalvar1() + ',' +
			str(flow.n_packet2) + ',' +
			str(sum(flow.n_byte2)) + ',' +
			'%.6f'%flow.t_start2 + ',' +
			'%.6f'%flow.t_end2 + ',' +
			'%.6f'%flow.getInterArrivaltime2() + ',' +
			'%.6f'%flow.getVarOfBytes2() + ',' +
			'%.6f'%flow.getInterArrivalvar2() + ',' + '\n')
	outfile.close()

def generateFlow(filename):
	sem.acquire()
	
	inputfile = open(filename)
	data = [line.strip() for line in inputfile]
	inputfile.close()
		
	packetlist = []
	for eachline in data:
		fields = eachline.split(',')
		fields.pop(2)
		packetlist.append(Packet(fields))
	
	outflowlist = packetsToFlows(packetlist, FLOWGAP)
	print 'flows in ' + filename + ' : ' + str(len(outflowlist))
	
	outfilename = filename[:-4]+'.flow.csv'	
	writeFlowsToFile(outflowlist, outfilename)

	print 'done writing to : ' + outfilename
	sem.release()

sem = MP.Semaphore(THREADLIMIT)


csvfiles = [i[:-5]+'.csv' for i in FILENAMES]
for filename in csvfiles:
	task = MP.Process(target = generateFlow, args = (filename,))
	task.start()

