import pickle
from enum import IntEnum
from random import shuffle
from read_dataset import readDataset


class field(IntEnum):
    SUBJECT = 0
    CONTENT_TYPE = 1
    BODY = 2
    IS_FRAUD = 3

# Returns an array of processed emails
# generated from their respective files
def generateDataset():

    # Reads email datasets and creates arrays of objects
    # of type [subject, content_type, body, is_fraud]
    try:
        benign_dataset = readDataset('./dataset/raw/benign_emails.txt', 0)
    except:
        print('ERROR: Cannot find benign emails dataset')
        print('Please download and unzip the enron email dataset indo ./dataset')
        print('and run "python3 process_enron.py"')

    try:
        fraud_dataset = readDataset('./dataset/raw/fraudulent_emails.txt', 1)
    except:
        print('ERROR: Cannot find fraudulent emails dataset, please download it')
        print('from kaggle and unzip it into ./dataset')

    # Joins datasets
    full_dataset = [*benign_dataset, *fraud_dataset]
    # Extracts only subject and is_fraud
    dataset = [[email[field.SUBJECT], email[field.IS_FRAUD]] for email in full_dataset]
    # Shuffles the array
    shuffle(dataset)
    return dataset


def getDataset80():
    # Tries to open existing dataset (saved as list)
    # if it does not exist, generates a new one
    try:
        dataset_file = open('./dataset/percentage-split/dataset_80.bin', 'rb')
    except:
        print('WARNING: 80% Dataset not found, generating new one')
        generateSplitDatasets()
        dataset_file = open('./dataset/percentage-split/dataset_80.bin', 'wb')

    dataset = pickle.load(dataset_file)
    return dataset


def getDataset20():
    # Tries to open existing dataset (saved as list)
    # if it does not exist, generates a new one
    try:
        dataset_file = open('./dataset/percentage-split/dataset_20.bin', 'rb')
    except:
        print('WARNING: 20% Dataset not found, generating new one')
        generateSplitDatasets()
        dataset_file = open('./dataset/percentage-split/dataset_20.bin', 'wb')

    dataset = pickle.load(dataset_file)
    return dataset


# Generates the percentage split dataset files
def generateSplitDatasets():
    print('Generating percentage split datasets')
    dataset = generateDataset()
    splitIndex = int(round(0.8*len(dataset)))
    dataset_80, dataset_20 = dataset[:splitIndex], dataset[splitIndex:]

    dataset_file = open('./dataset/percentage-split/dataset_80.bin', 'wb')
    pickle.dump(dataset_80, dataset_file)
    dataset_file.close()

    dataset_file = open('./dataset/percentage-split/dataset_20.bin', 'wb')
    pickle.dump(dataset_20, dataset_file)
    dataset_file.close()


if __name__ == '__main__':
    generateSplitDatasets()
