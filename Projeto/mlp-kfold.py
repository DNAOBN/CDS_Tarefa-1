from utils import *
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from kfold import getKFoldDatasets

# Plotting Confusion Matrix and ROC curve
fig, (confusion_matrix_axes, roc_axes) = plt.subplots(1, 2)

for i in range(0, 5):

  train_dataset, test_dataset = getKFoldDatasets(i)

  dataset = ClassifierDataset(train_dataset, test_dataset)


  # Creating tf-idf training and test matrix
  tfIdfVectorizer=TfidfVectorizer(use_idf=True)
  train_matrix = tfIdfVectorizer.fit_transform(dataset.training_data).toarray()
  test_matrix = tfIdfVectorizer.transform(dataset.test_data).toarray()


  # Training KNN model
  print('Starting fit')
  clf = MLPClassifier(random_state=1, max_iter=300, hidden_layer_sizes=(20, 20, 20))
  clf.fit(train_matrix, dataset.training_target)
  print('Finished fit')


  # Predicting test dataset classification
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
  metrics.plot_confusion_matrix(clf, test_matrix, dataset.test_target, ax = confusion_matrix_axes)
  metrics.plot_roc_curve(clf, test_matrix, dataset.test_target, ax = roc_axes)
plt.show()
