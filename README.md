# Botnet-Detector
A tool used to detect botnet based on existing P2P botnet packet dataset and health packet dataset. Using machine learning to differentiate botnet trace out of normal trace.

* Extract features with [Tshark](https://linux.die.net/man/1/tshark) and [numpy](http://www.numpy.org/)
* Train and generate result with [sklearn extraTreesClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)
* High true rate of 99%

## To use this tool

1. Put a healthy pcap dataset and a botnet/suspicious pcap dataset in root
2. Modify `all.sh`, in the fourth line, change second and third parameters into `healthy pcap filename`+`.features.csv` and `pcap filename`+`.features.csv`
3. In the terminal, use command `. all.sh`
