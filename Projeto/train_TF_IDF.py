from sklearn.feature_extraction.text import TfidfVectorizer
from read_dataset import readDataset
import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import neighbors
import matplotlib.pyplot as plt
import seaborn as sns


dataset_path = './dataset/benign_emails.txt'

is_dataset_benign = 1 if dataset_path.find('benign') != -1 else 0
dataset = readDataset(dataset_path, is_dataset_benign)
# print(list(map(lambda a: a[0], dataset)))

tfIdfVectorizer=TfidfVectorizer(use_idf=True)
tfIdf = tfIdfVectorizer.fit_transform([email[0] for email in dataset])
# print(tfIdf.T)
# df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
# df = df.sort_values('TF-IDF', ascending=False)
# print (df.head(25))

# model = Word2Vec([[word.lower() for word in email[0].split(' ')] for email in dataset],size=2, min_count=1)

# print(model.wv['dave'])


n_neighbors = 15

# we only take the first two features. We could avoid this ugly
# slicing by using a two-dim dataset
X = tfIdf[0].T.todense()#[model.wv[a] for a in model.wv.vocab]
print(X)
y = tfIdfVectorizer.get_feature_names()#range(0, len(model.wv.vocab))

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
cmap_bold = ['darkorange', 'c', 'darkblue']

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = min(list(map(lambda x: x[0], X))) - 1, max(list(map(lambda x: x[0], X))) + 1
    y_min, y_max = min(list(map(lambda x: x[1], X))) - 1, max(list(map(lambda x: x[1], X))) + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    sns.scatterplot(x=list(map(lambda x: x[0], X)), y=list(map(lambda x: x[1], X)),
                    palette=cmap_bold, alpha=1.0, edgecolor="black")
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))
    plt.xlabel('0')
    plt.ylabel('1')

plt.show()