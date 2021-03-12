from enum import IntEnum
from sklearn.feature_extraction.text import TfidfVectorizer
from read_dataset import readDataset
# from gensim.models import Word2Vec
from sklearn import neighbors
from random import shuffle
import pickle
from sklearn import ensemble
from sklearn import neighbors, svm, metrics
import matplotlib.pyplot as plt

class field(IntEnum):
    SUBJECT = 0
    CONTENT_TYPE = 1
    BODY = 2
    IS_BENIGN = 3

def generateDataset():
    # Arrays of [subject, content_type, body, is_benign]
    benign_dataset = readDataset('./dataset/benign_emails.txt', 1)
    fraud_dataset = readDataset('./dataset/fraudulent_emails.txt', 0)

    # get an array of [subject, is_benign] objects
    benign_bodies = [[email[field.SUBJECT], email[field.IS_BENIGN]] for email in benign_dataset]
    fraud_bodies  = [[email[field.SUBJECT], email[field.IS_BENIGN]] for email in fraud_dataset]

    # joins datasets and shuffles it
    dataset = [*benign_bodies, *fraud_bodies]
    shuffle(dataset)
    return dataset

# Tries to open existing dataset (saved as list)
# if it does not exist, generates a new one
try:
    dataset_file = open('./dataset/full_dataset.bin', 'rb')
    dataset = pickle.load(dataset_file)
except:
    dataset = generateDataset()
    dataset_file = open('./dataset/full_dataset.bin', 'wb')
    pickle.dump(dataset, dataset_file)

# Splits dataset in 80 - 20
splitIndex = int(round(0.8*len(dataset)))
train_dataset, test_dataset = dataset[:splitIndex], dataset[splitIndex:]

train_data_array   = [email[0] for email in train_dataset]
train_target_array = [email[1] for email in train_dataset]

test_data_array   = [email[0] for email in test_dataset]
test_target_array = [email[1] for email in test_dataset]


tfIdfVectorizer=TfidfVectorizer(use_idf=True)
train_matrix = tfIdfVectorizer.fit_transform(train_data_array).toarray()
# print(tfIdf[:3])
# print(tfIdf.toarray()[:3])
# print(tfIdfVectorizer.get_feature_names())
# df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
# df = df.sort_values('TF-IDF', ascending=False)
# print (df.head(25))

# # model = Word2Vec([[word.lower() for word in email[0].split(' ')] for email in dataset],size=2, min_count=1)

# # print(model.wv['dave'])


n_neighbors = 15

print('Starting fit')
clf = neighbors.KNeighborsClassifier(n_neighbors)
clf.fit(train_matrix, train_target_array)
print('Finished fit')



# aux=TfidfVectorizer(use_idf=True)
test_matrix = tfIdfVectorizer.transform(test_data_array).toarray()
print('Starting prediction')
result = clf.predict(test_matrix)
print('Finished prediction')
print('Starting score calculation')
score = 0
# predicted_real
fraud_fraud = 0
fraud_benign = 0
benign_benign = 0
benign_fraud = 0
# print(list(result))
# print(test_target_array)
for predicted, real in zip(list(result), test_target_array):
    fraud_fraud += 1 if (predicted == 0 and real == 0) else 0
    fraud_benign += 1 if (predicted == 0 and real == 1) else 0
    benign_benign += 1 if (predicted == 1 and real == 1) else 0
    benign_fraud += 1 if (predicted == 1 and real == 0) else 0
    score += 1 if predicted == real else 0

print(score/len(result))

metrics.plot_roc_curve(clf, test_matrix, test_target_array)  
plt.show() 