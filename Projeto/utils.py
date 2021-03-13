from sklearn import metrics

def splitDataset(data, percentage=0.8):
    split_index = int(round(percentage*len(data)))

    section_1 = data[:split_index]
    section_2 = data[split_index:]

    return [section_1, section_2]

def extractDataAndTargetValues(dataset):
    data_values   = [value[0] for value in dataset]
    target_values = [value[1] for value in dataset]

    return [data_values, target_values]


class ClassifierDataset():
    def __init__(self, data, aux_data=None):
        if aux_data == None:
            training_dataset, test_dataset = splitDataset(data)
        else:
            training_dataset = data
            test_dataset = aux_data
            data = [*training_dataset, *test_dataset]

        test_data, test_target = extractDataAndTargetValues(test_dataset)
        training_data, training_target = extractDataAndTargetValues(training_dataset)

        self.test_result = None
        self.complete_data = data
        self.test_data = test_data
        self.test_target = test_target
        self.training_data = training_data
        self.training_target = training_target

    def setTestResult(self, result):
        self.test_result = result

    def getResultMetrics(self):
        if self.test_result is None:
            return [None, None, None]

        error = metrics.mean_absolute_error(self.test_target, self.test_result)
        precision_score = metrics.precision_score(self.test_target, self.test_result)
        confusion_matrix = metrics.confusion_matrix(self.test_target, self.test_result).ravel()

        return [precision_score, error, confusion_matrix]


def printPrecisionScore(precision_score):
    print(f'Precision Score: {precision_score}')

def printMeanAbsoluteError(error):
    print(f'Mean Absolute Error: {error}')

# @param confusion_matrix must be a tuple with the following form
#   (true_negative, false_positive, false_negative, true_positive)
def printConfusionMatrix(confusion_matrix):
    if confusion_matrix is None:
        print('printConfusionMatrix - Invalid confusion matrix')

    benign_benign, benign_fraud, fraud_benign, fraud_fraud = confusion_matrix

    print(f'\n  CONFUSION   |   [PREDICTED]  |')
    print(f'   MATRIX     | Benign | Fraud |')
    print(f'[REAL] Benign | {benign_benign: 6} | {benign_fraud: 5} |')
    print(f'[REAL]  Fraud | {fraud_benign: 6} | {fraud_fraud: 5} |')
