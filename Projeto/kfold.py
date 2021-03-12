import pickle
from os import mkdir
from percentage_split import getDataset80


def getKFoldDatasets(testFolder):
    try:
        train_dataset = []
        for j in range(0, 5):
            dataset_file = open(f'./dataset/k-fold/{j}', 'rb')
            if j == testFolder:
                test_dataset = pickle.load(dataset_file)
            else:
                train_dataset += pickle.load(dataset_file)
    except:
        print('ERROR: Generate k-fold dataset with "python3 kfold.py"')
        quit()
    return train_dataset, test_dataset


dataset = getDataset80()
k_dataset = [None, None, None, None, None]

splitIndex = int(round(0.20*len(dataset)))

for i in range(0, 5):
    startIndex = i * splitIndex
    endIndex = (i+1) * splitIndex if i < 4 else len(dataset)
    k_dataset[i] = dataset[startIndex : endIndex]

for i in range(0, len(k_dataset)):
    try:
        mkdir('./dataset/k-fold')
    except:
        None
    file = open(f'./dataset/k-fold/{i}', 'wb')
    pickle.dump(k_dataset[i], file)
