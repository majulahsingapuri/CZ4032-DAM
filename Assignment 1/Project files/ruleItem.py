import functools
from functools import total_ordering
  

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
    '''def __eq__(self,other):
        return self.confidence==other.confidence and self.support==other.support and len(self.condSet)==len(other.condSet)
    def __hash__(self):
        return hash(self.confidence)+hash(self.support)+hash(len(self.condSet))
    def __gt__(self,other):
        if (other==None):
            return True
        if (self.confidence>other.confidence):
            return True
        if (self.confidence==other.confidence and self.support>other.support):
            return True
        if (self.confidence==other.confidence and self.support==other.support and len(self.condSet)<len(self.condSet)):
            return True
        return False
    '''
    def print(self):
        output = ''
        for item in self.condSet:
            output += '(' + str(item) + ', ' + str(self.condSet[item]) + '), '
        output = output[:-2]
        print( '<({' + output + '}, ' + str(self.condSupportCount) + '), (' + '(class, ' + str(self.classLabel) + '), ' + str(self.ruleSupportCount) + ')>')


        



    # print out rule
    def printRule(self):
        output = ''
        for item in self.condSet:
            output += '(' + str(item) + ', ' + str(self.condSet[item]) + '), '
        output = '{' + output[:-2] + '}'
        print(output + ' -> (class, ' + str(self.classLabel) + ')')
