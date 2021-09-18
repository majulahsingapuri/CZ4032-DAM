class RuleItem:
    def __init__(self, condSet, classLabel, dataset):
        self.condSet = condSet
        self.classLabel = classLabel
        self.condSupportCount, self.ruleSupportCount = self._getSupportCount(dataset)
        self.support = self._getSupport(len(dataset))
        self.confidence = self._getConfidence()

    # calculate condsupCount and rulesupCount
    def _getSupportCount(self, dataset):
        condSupportCount = 0
        ruleSupportCount = 0
        for case in dataset:
            contained = True
            for index in self.condSet:
                if self.condSet[index] != case[index]:
                    contained = False
                    break
            if contained:
                condSupportCount += 1
                if self.classLabel == case[-1]:
                    ruleSupportCount += 1
        return condSupportCount, ruleSupportCount

    # calculate support count
    def _getSupport(self, datasetSize):
        return self.ruleSupportCount / datasetSize

    # calculate confidence
    def _getConfidence(self):
        if self.condSupportCount != 0:
            return self.ruleSupportCount / self.condSupportCount
        else:
            return 0

    # print out the ruleitem
    def print(self):
        output = ''
        for item in self.condSet:
            output += '(' + str(item) + ', ' + str(self.condSet[item]) + '), '
        output = output[:-2]
        print('<({' + output + '}, ' + str(self.condSupportCount) + '), (' +
              '(class, ' + str(self.classLabel) + '), ' + str(self.ruleSupportCount) + ')>')

    # print out rule
    def print_rule(self):
        output = ''
        for item in self.condSet:
            output += '(' + str(item) + ', ' + str(self.condSet[item]) + '), '
        output = '{' + output[:-2] + '}'
        print(output + ' -> (class, ' + str(self.classLabel) + ')')
