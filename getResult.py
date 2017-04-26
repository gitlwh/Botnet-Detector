from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
	#get all data
	#devide features and label
trainingData = open("training.csv")
trainingLabels = []
trainingFeatures = []
for line in trainingData.readlines():
	features = line.strip().split(',')
	print features
	trainingLabels.append(int(features.pop()))
	trainingFeatures.append([float(i) for i in features])

print "hello"

testingData = open("test.csv")
testingLabels = []
testingFeatures = []
for line in testingData.readlines():
	features = line.strip().split(',')
	print features
	testingLabels.append(0)
	features.pop()
	testingFeatures.append([float(i) if i!='' else 0 for i in features])


print testingFeatures
print testingLabels
print "training extra trees forest"
clf = ExtraTreesClassifier(n_estimators=1000, n_jobs=8, min_samples_split=10)
clf.fit(trainingFeatures, trainingLabels)
pred_label_test = clf.predict(testingFeatures)
np.reshape(pred_label_test,(-1,1))
testingStandardData = open("testStandard.csv")
true = 0
false = 0
n = 0
for line in testingStandardData.readlines():
	print pred_label_test[n], line
	if pred_label_test[n]==int(line.strip().split(',')[-1]):
		true += 1
	else:
		false += 1
	n += 1

print "true"+str(true)+";false"+str(false)+"ratio:"+str(float(true)/(false+true))