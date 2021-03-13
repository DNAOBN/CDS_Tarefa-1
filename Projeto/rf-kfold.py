import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from kfold import getKFoldDatasets
from utils import *
from percentage_split import *

# Plotting Confusion Matrix and ROC curve
fig, roc_axes = plt.subplots(1, 1)
fig, confusion_matrix_axes = plt.subplots(1, 5)

for i in range(0, 5):

  train_dataset, test_dataset = getKFoldDatasets(i)

  dataset = ClassifierDataset(train_dataset, test_dataset)


  # Creating tf-idf training and test matrix
  tfIdfVectorizer=TfidfVectorizer(use_idf=True)
  training_matrix = tfIdfVectorizer.fit_transform(dataset.training_data).toarray()
  test_matrix = tfIdfVectorizer.transform(dataset.test_data).toarray()


  # Training random forest model
  print('Starting fit')
  clf = RandomForestClassifier(max_depth=None, random_state=0)
  clf.fit(training_matrix, dataset.training_target)
  print('Finished fit')


  # Predicts test dataset classification
  print('Starting prediction')
  test_result = clf.predict(test_matrix)
  dataset.setTestResult(test_result)
  print('Finished prediction')


  # Printing metrics
  print('\n------------------------------------------------')
  print(f'Classification results {i} for 80% of full dataset')
  print('------------------------------------------------')
  precision_score, error, confusion_matrix = dataset.getResultMetrics()
  printPrecisionScore(precision_score)
  printMeanAbsoluteError(error)
  printConfusionMatrix(confusion_matrix)


  # Plotting Confusion Matrix and ROC curve
  metrics.plot_confusion_matrix(clf, test_matrix, dataset.test_target, ax = confusion_matrix_axes[i])
  metrics.plot_roc_curve(clf, test_matrix, dataset.test_target, ax = roc_axes)


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
  fig_20, (confusion_matrix_axes_20, roc_axes_20) = plt.subplots(1, 2)
  fig_20.suptitle('Test results with 20% of full dataset')

  metrics.plot_confusion_matrix(clf, test_matrix, test_target, ax = confusion_matrix_axes_20,
                                labels=[0, 1], display_labels=['Benign', 'Fraud'])
  metrics.plot_roc_curve(clf, test_matrix, test_target, ax = roc_axes_20)
plt.show()
