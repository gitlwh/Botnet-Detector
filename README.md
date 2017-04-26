# Botnet-Detector
A tool used to detect botnet based on existing P2P botnet packet dataset and health packet dataset. Using machine learning to differentiate botnet trace out of normal trace.

* Extract features with [Tshark](https://linux.die.net/man/1/tshark) and [numpy](http://www.numpy.org/)
* Train and generate result with [sklearn extraTreesClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)
* High true rate of 99%

## System combination

1. `dataExtraction.py`: Extracting packet data from pcap files and save as `name.csv`
2. `generateFlow.py`: Combining packets with same sent IP and receive IP into flows and save flows into `name.flow.csv`
3. `featuresExtraction.py`: Extracting features from flows and save as `name.features.csv`
4. `flowMix`: Generate train and test file by combining normal dataset and malicious dataset and save as `test.csv`, `train.csv` and `testStandard.csv`
5. `getResult`: To train and get result and get true rate.


## To use this tool

1. Put a healthy pcap dataset and a botnet/suspicious pcap dataset in root
2. Modify `constants.py`, put the file names you want to use in FILENAMES.
3. Modify `all.sh`, in the fourth line, change second and third parameters into `healthy pcap filename`+`.features.csv` and `malicious pcap filename`+`.features.csv`. In my program, I use half total data to train and anothor half to test. You can modify the ratio on your own.
4. In the terminal, use command `. all.sh`
