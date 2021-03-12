from sklearn import metrics

def split80_20(data):
    split_index = int(round(0.8*len(data)))

    section80 = data[:split_index]
    section20 = data[split_index:]

    return [section80, section20]

def extractDataAndTargetValues(dataset):
    data_values   = [value[0] for value in dataset]
    target_values = [value[1] for value in dataset]

    return [data_values, target_values]


class ClassifierDataset():
    def __init__(self, data):
        training_dataset, test_dataset = split80_20(data)

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
