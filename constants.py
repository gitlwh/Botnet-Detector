FILENAMES = ['kelihos.pcap','mypcap.pcap']
parameters = '-t e -T fields -E separator=, -e ip.src -e ip.dst -e ip.proto -e frame.time_epoch -e tcp.len -e udp.length \
-Y "(ip.proto==6)||(ip.proto==17)"'
parameternum = 6
THREADLIMIT = 10
UDP_HEADERLENGTH = 8
FLOWGAP = 1 * 60 * 60