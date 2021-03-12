import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from kfold import getDataset80
from utils import *

# Building dataset
complete_dataset = getDataset80()
dataset = ClassifierDataset(complete_dataset)


# Creating tf-idf training and test matrix
tfIdfVectorizer=TfidfVectorizer(use_idf=True)
training_matrix = tfIdfVectorizer.fit_transform(dataset.training_data).toarray()
test_matrix = tfIdfVectorizer.transform(dataset.test_data).toarray()


# Training MLP model
print('Starting fit')
clf = MLPClassifier(random_state=1, max_iter=300, hidden_layer_sizes=(20, 20, 20))
clf.fit(training_matrix, dataset.training_target)
print('Finished fit')


# Predicts test dataset classification
print('Starting prediction')
test_result = clf.predict(test_matrix)
dataset.setTestResult(test_result)
print('Finished prediction')


# Printing metrics
precision_score, error, confusion_matrix = dataset.getResultMetrics()
printPrecisionScore(precision_score)
printMeanAbsoluteError(error)
printConfusionMatrix(confusion_matrix)


# Plotting Confusion Matrix and ROC curve
fig, (confusion_matrix_axes, roc_axes) = plt.subplots(1, 2)

metrics.plot_confusion_matrix(clf, test_matrix, dataset.test_target, ax = confusion_matrix_axes)
metrics.plot_roc_curve(clf, test_matrix, dataset.test_target, ax = roc_axes)
plt.show()
