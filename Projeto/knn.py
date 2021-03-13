import matplotlib.pyplot as plt
from utils import *
from sklearn import metrics, neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from percentage_split import *

# Building dataset
complete_dataset = getDataset80()
dataset = ClassifierDataset(complete_dataset)


# Creating tf-idf training and test matrix
tfIdfVectorizer=TfidfVectorizer(use_idf=True)
training_matrix = tfIdfVectorizer.fit_transform(dataset.training_data).toarray()
test_matrix = tfIdfVectorizer.transform(dataset.test_data).toarray()


# Training KNN model
print('Starting fit')
n_neighbors = 2
clf = neighbors.KNeighborsClassifier(n_neighbors)
clf.fit(training_matrix, dataset.training_target)
print('Finished fit')


# Predicting test dataset classification
print('Starting prediction')
test_result = clf.predict(test_matrix)
dataset.setTestResult(test_result)
print('Finished prediction')


# Printing metrics
print('\n-------------------------------------------------------')
print('Classification results for 20% of 80% of full dataset')
print('-------------------------------------------------------')
precision_score, error, confusion_matrix = dataset.getResultMetrics()
printPrecisionScore(precision_score)
printMeanAbsoluteError(error)
printConfusionMatrix(confusion_matrix)


# Plotting Confusion Matrix and ROC curve
fig, (confusion_matrix_axes, roc_axes) = plt.subplots(1, 2)
fig.suptitle('Test results with 20% of 80% of full dataset')

metrics.plot_confusion_matrix(clf, test_matrix, dataset.test_target, ax = confusion_matrix_axes,
                              labels=[0, 1], display_labels=['Benign', 'Fraud'])
metrics.plot_roc_curve(clf, test_matrix, dataset.test_target, ax = roc_axes)
plt.show()



# ====================================
# Test with other 20% of whole dataset
# ====================================

# Extract data and class and convert to TF-IDF
test_data, test_target = extractDataAndTargetValues(getDataset20())
test_matrix = tfIdfVectorizer.transform(test_data).toarray()

# Predict test dataset classification
print('Starting prediction')
test_result = clf.predict(test_matrix)
print('Finished prediction')

# Calculate and print error, precision score and the confusion matrix
error = metrics.mean_absolute_error(test_target, test_result)
precision_score = metrics.precision_score(test_target, test_result)
confusion_matrix = metrics.confusion_matrix(test_target, test_result).ravel()

print('\n----------------------------------------------')
print('Classification results for 20% of full dataset')
print('----------------------------------------------')
printPrecisionScore(precision_score)
printMeanAbsoluteError(error)
printConfusionMatrix(confusion_matrix)


# Plotting Confusion Matrix and ROC curve
fig, (confusion_matrix_axes, roc_axes) = plt.subplots(1, 2)
fig.suptitle('Test results with 20% of full dataset')

metrics.plot_confusion_matrix(clf, test_matrix, test_target, ax = confusion_matrix_axes,
                              labels=[0, 1], display_labels=['Benign', 'Fraud'])
metrics.plot_roc_curve(clf, test_matrix, test_target, ax = roc_axes)
plt.show()