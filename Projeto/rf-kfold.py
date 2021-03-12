import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from kfold import getKFoldDatasets

fig, axes = plt.subplots(1, 1)

for i in range(0, 5):
    
  train_dataset, test_dataset = getKFoldDatasets(i)

  # Separates data and target values
  train_data_array   = [email[0] for email in train_dataset]
  train_target_array = [email[1] for email in train_dataset]

  test_data_array   = [email[0] for email in test_dataset]
  test_target_array = [email[1] for email in test_dataset]


  # Creates training tf-idf matrix
  tfIdfVectorizer=TfidfVectorizer(use_idf=True)
  train_matrix = tfIdfVectorizer.fit_transform(train_data_array).toarray()


  print('Starting fit')
  clf = RandomForestClassifier(max_depth=None, random_state=0)
  clf.fit(train_matrix, train_target_array)
  print('Finished fit')

  # Creates testing tf-idf matrix
  test_matrix = tfIdfVectorizer.transform(test_data_array).toarray()

  # Predicts test dataset classification
  print('Starting prediction')
  result = clf.predict(test_matrix)
  print('Finished prediction')

  score = 0

  # predicted_real
  fraud_fraud = 0
  fraud_benign = 0
  benign_benign = 0
  benign_fraud = 0

  for predicted, real in zip(list(result), test_target_array):
      fraud_fraud += 1 if (predicted == 0 and real == 0) else 0
      fraud_benign += 1 if (predicted == 0 and real == 1) else 0
      benign_benign += 1 if (predicted == 1 and real == 1) else 0
      benign_fraud += 1 if (predicted == 1 and real == 0) else 0
      score += 1 if predicted == real else 0

  print(f'Precision: {score/len(result)}')
  error = metrics.mean_absolute_error(test_target_array, result)
  print(f'Error: {error}')

  print(['       ', 'Fraude', 'Benigno'])
  print(['Fraude ', fraud_fraud, benign_fraud])
  print(['Benigno', benign_fraud, benign_benign])

  metrics.plot_roc_curve(clf, test_matrix, test_target_array, ax=axes)
  
plt.show()

