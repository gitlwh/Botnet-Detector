from constants import *
from packetStructure import *
import sys

outfile1 = open("training.csv",'w')
outfile2 = open("test.csv",'w')
outfile3 = open("testStandard.csv",'w')
f1 = open(sys.argv[1])
f2 = open(sys.argv[2])
ratio = float(sys.argv[3])
n1 = sum(1 for line in f1)
a1 = ratio * n1
n2 = sum(1 for line in f2)
a2 = ratio * n2
i1 = 0
i2 = 0
print n1,n2
print "ooo"
f1 = open(sys.argv[1])
f2 = open(sys.argv[2])
line = f1.readline().strip()
while line!='':
	if i1 < a1:
		outfile1.write(line[:-1]+",1"+"\n")
	else:
		outfile3.write(line[:-1]+",1"+"\n")
		outfile2.write(line+"\n")
	i1+=1
	line = f1.readline().strip()

line = f2.readline().strip()
while line!='':
	if i2 < a2:
		outfile1.write(line[:-1]+",0"+"\n")
	else:
		outfile3.write(line[:-1]+",0"+"\n")
		outfile2.write(line+"\n")
	i2+=1
	line = f2.readline().strip()

