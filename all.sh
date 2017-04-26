#!/bin/sh

python dataExtraction.py
python generateFlow.py
python featuresExtraction.py
python flowMix.py mypcap.features.csv zeroaccess.features.csv 0.5
python getResult.py
#python plot.py
