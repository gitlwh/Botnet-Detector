import socket
import numpy as np
#defines properties of a packet
class Packet:
	def __init__(self,fields):
		if fields == None:
			self.source = None
			self.dest = None
			self.timestamp = None
			self.size = 0
			self.key = None
		else:
			self.source = socket.inet_aton(fields[0])
			self.dest = socket.inet_aton(fields[1])
			self.timestamp = float(fields[2])
			self.size = int(fields[3])
			if self.source < self.dest:
				self.key = self.source + self.dest
			else:
				self.key = self.dest + self.source


class Flow:
	#constructor of default flow
	def __init__(self,firstpacket):
		if firstpacket == None:
			self.ip1 = None
			self.ip2 = None
			self.key = None
			self.n_packet1 = 0
			self.n_byte1 = []
			self.t_start1 = 0
			self.t_end1 = 0	
			self.t_interarrival1 = []
			self.n_packet2 = 0
			self.n_byte2 = []
			self.t_start2 = 0
			self.t_end2 = 0
			self.t_interarrival2 = []
		else:
			if firstpacket.source < firstpacket.dest:
				self.ip1 = firstpacket.source
				self.ip2 = firstpacket.dest
				self.n_packet1 = 1
				self.n_byte1 = [firstpacket.size]
				self.t_start1 = firstpacket.timestamp
				self.t_end1 = firstpacket.timestamp
				self.t_interarrival1 = []						
				self.n_packet2 = 0
				self.n_byte2 = []
				self.t_start2 = 0
				self.t_end2 = 0
				self.t_interarrival2 = []
			else:
				self.ip1 = firstpacket.dest
				self.ip2 = firstpacket.source
				self.n_packet1 = 0
				self.n_byte1 = []
				self.t_start1 = 0
				self.t_end1 = 0
				self.t_interarrival1 = []
				self.n_packet2 = 1			
				self.n_byte2 = [firstpacket.size]			
				self.t_start2 = firstpacket.timestamp
				self.t_end2 = firstpacket.timestamp
				self.t_interarrival2 = []			
			self.key = firstpacket.key
	
	#add a packet to the current flow (by changing volume and duration)
	def addPacket(self,packet):
		if packet.source == self.ip1 and packet.dest == self.ip2:			
			
			#initialize flow if not initialized
			if self.n_packet1 == 0:
				self.t_start1 = packet.timestamp
				self.t_end1 = packet.timestamp
				self.n_packet1 += 1
				self.n_byte1.append(packet.size)
				return

			if self.t_end1 < packet.timestamp:
				self.t_interarrival1.append(packet.timestamp-self.t_end1)
				self.t_end1 = packet.timestamp
			elif self.t_start1 > packet.timestamp:
				self.t_interarrival1.append(self.t_start1-packet.timestamp)
				self.t_start1 = packet.timestamp
			self.n_packet1 += 1
			self.n_byte1.append(packet.size)			
		
		elif packet.source == self.ip2 and packet.dest == self.ip1:
			
			#initialize flow if not initialized
			if self.n_packet2 == 0:
				self.t_start2 = packet.timestamp
				self.t_end2 = packet.timestamp
				self.n_packet2 += 1
				self.n_byte2.append(packet.size)
				return
			
			if self.t_end2 < packet.timestamp:
				self.t_interarrival2.append(packet.timestamp-self.t_end2)
				self.t_end2 = packet.timestamp
			elif self.t_start2 > packet.timestamp:
				self.t_interarrival2.append(self.t_start2-packet.timestamp)
				self.t_start2 = packet.timestamp
			self.n_packet2 += 1
			self.n_byte2.append(packet.size)

		else:
			raise Exception('packet does not belong to flow')
	



	def getDurationInSeconds(self):
		return self.getEnd() - self.getStart()

	def getInterArrivaltime(self):
		combined = (self.t_interarrival1+self.t_interarrival2).sort()
		if len(combined) > 0:
			return combined[len(combined)/2]
		return 0	
	
	def getInterArrivaltime1(self):
		self.t_interarrival1.sort()
		if len(self.t_interarrival1) > 0:
			return self.t_interarrival1[len(self.t_interarrival1)/2]
		return 0

	def getInterArrivalvar1(self):
		a = np.var(self.t_interarrival1)
		if np.isnan(a):
			return 0
		return a

	def getInterArrivaltime2(self):
		self.t_interarrival2.sort()
		if len(self.t_interarrival2) > 0:
			return self.t_interarrival2[len(self.t_interarrival2)/2]
		return 0	

	def getInterArrivalvar2(self):
		a = np.var(self.t_interarrival2)
		if np.isnan(a):
			return 0
		return a
	
	def getNoOfBytes(self):
		return sum(sum(self.n_byte1),sum(self.n_byte2))

	def getVarOfBytes1(self):
		a = np.var(self.n_byte1)
		if np.isnan(a):
			return 0
		return a

	def getVarOfBytes2(self):
		a = np.var(self.n_byte2)
		if np.isnan(a):
			return 0
		return a

	def getNoOfPackets(self):
		return self.n_packet1 + self.n_packet2

	def getStart(self):
		temp =  min(self.t_start1, self.t_start2)
		if temp == 0:
			return self.t_start1 + self.t_start2
		else:
			return temp

	def getEnd(self):
		return max(self.t_end1, self.t_end2)