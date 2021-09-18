from ruleItem import RuleItem


class FrequentRuleItem:
    def __init__(self):
        self.frequentRuleItemSet = set()

    # get size of set
    def getSize(self):
        return len(self.frequentRuleItemSet)

    # add a new RuleItem into set
    def add(self, ruleItem):
        exists = False
        for item in self.frequentRuleItemSet:
            if item.classLabel == ruleItem.classLabel:
                if item.condSet == ruleItem.condSet:
                    exists = True
                    break
        if not exists:
            self.frequentRuleItemSet.add(ruleItem)

    # append set of ruleitems
    def append(self, sets):
        for item in sets.frequentRuleItems:
            self.add(item)

    # print out all frequent ruleitems
    def print(self):
        for item in self.frequentRuleItemSet:
            item.print()


class CAR:
    def __init__(self):
        self.rules = set()
        self.prunedRules = set()

    # print out all rules
    def printRule(self):
        for item in self.rules:
            item.printRule()

    # print out all pruned rules
    def printPrunedRules(self):
        for item in self.prunedRules:
            item.printRule()

    # add a new rule (frequent & accurate), save the RuleItem with the highest confidence when having the same condset
    def _add(self, ruleItem, minsup, minConf):
        if ruleItem.support >= minsup and ruleItem.confidence >= minConf:
            if ruleItem in self.rules:
                return
            for item in self.rules:
                if item.condSet == ruleItem.condSet and item.confidence < ruleItem.confidence:
                    self.rules.remove(item)
                    self.rules.add(ruleItem)
                    return
                elif item.condSet == ruleItem.condSet and item.confidence >= ruleItem.confidence:
                    return
            self.rules.add(ruleItem)

    # convert frequent ruleitems into car
    def genRules(self, frequentRuleItems, minsup, minConf):
        for item in frequentRuleItems.frequentRuleItemSet:
            self._add(item, minsup, minConf)

    # prune rules
    def pruneRules(self, dataset):
        for rule in self.rules:
            prunedRule = prune(rule, dataset)

            exists = False
            for rule in self.prunedRules:
                if rule.classLabel == prunedRule.classLabel:
                    if rule.condSet == prunedRule.condSet:
                        exists = True
                        break

            if not exists:
                self.prunedRules.add(prunedRule)

    # union new car into rules list
    def append(self, car, minsup, minConf):
        for item in car.rules:
            self._add(item, minsup, minConf)


# try to prune rule
def prune(rule, dataset):
    import sys
    minRuleError = sys.maxsize
    prunedRule = rule

    # prune rule recursively
    def findPruneRule(thisRule):
        nonlocal minRuleError
        nonlocal prunedRule
        def is_satisfy(datacase, rule):
            for item in rule.condSet:
                if datacase[item] != rule.condSet[item]:
                    return None
            if datacase[-1] == rule.classLabel:
                return True
            else:
                return False

        # calculate how many errors the rule r make in the dataset
        def ruleError(r):
            errors = 0
            for case in dataset:
                if is_satisfy(case, r) == False:
                    errors += 1
            return errors

        ruleError = ruleError(thisRule)
        if ruleError < minRuleError:
            minRuleError = ruleError
            prunedRule = thisRule
        thisRuleCondSet = list(thisRule.condSet)
        if len(thisRuleCondSet) >= 2:
            for attribute in thisRuleCondSet:
                tempCondSet = dict(thisRule.condSet)
                tempCondSet.pop(attribute)
                tempRule = RuleItem(tempCondSet, thisRule.classLabel, dataset)
                tempRuleError = ruleError(tempRule)
                if tempRuleError <= minRuleError:
                    minRuleError = tempRuleError
                    prunedRule = tempRule
                    if len(tempCondSet) >= 2:
                        findPruneRule(tempRule)

    findPruneRule(rule)
    return prunedRule


# invoked by candidateGenerator, join two items to generate candidate
def join(item1, item2, dataset):
    if item1.classLabel != item2.classLabel:
        return None
    category1 = set(item1.condSet)
    category2 = set(item2.condSet)
    if category1 == category2:
        return None
    intersect = category1 & category2
    for item in intersect:
        if item1.condSet[item] != item2.condSet[item]:
            return None
    category = category1 | category2
    new_condSet = dict()
    for item in category:
        if item in category1:
            new_condSet[item] = item1.condSet[item]
        else:
            new_condSet[item] = item2.condSet[item]
    new_ruleitem = RuleItem(new_condSet, item1.classLabel, dataset)
    return new_ruleitem


# similar to Apriori-gen in algorithm Apriori
def candidateGenerator(frequentRuleItems, dataset):
    returnedFrequentRuleItems = FrequentRuleItem()
    for item1 in frequentRuleItems.frequentRuleItemSet:
        for item2 in frequentRuleItems.frequentRuleItemSet:
            new_ruleitem = join(item1, item2, dataset)
            if new_ruleitem:
                returnedFrequentRuleItems.add(new_ruleitem)
                if returnedFrequentRuleItems.getSize() >= 1000:      # not allow to store more than 1000 ruleitems
                    return returnedFrequentRuleItems
    return returnedFrequentRuleItems


# main method, implementation of CBA-RG algorithm
def rule_generator(dataset, minsup, minConf):
    frequentRuleItems = FrequentRuleItem()
    car = CAR()

    # get large 1-ruleitems and generate rules
    classLabel = set([x[-1] for x in dataset])
    for column in range(0, len(dataset[0])-1):
        distinct_value = set([x[column] for x in dataset])
        for value in distinct_value:
            condSet = {column: value}
            for classes in classLabel:
                ruleItem = RuleItem(condSet, classes, dataset)
                if ruleItem.support >= minsup:
                    frequentRuleItems.add(ruleItem)
    car.genRules(frequentRuleItems, minsup, minConf)
    cars = car

    lastCARsNumber = 0
    currentCARsNumber = len(cars.rules)
    while frequentRuleItems.getSize() > 0 and currentCARsNumber <= 2000 and \
                    (currentCARsNumber - lastCARsNumber) >= 10:
        candidate = candidateGenerator(frequentRuleItems, dataset)
        frequentRuleItems = FrequentRuleItem()
        car = CAR()
        for item in candidate.frequentRuleItemSet:
            if item.support >= minsup:
                frequentRuleItems.add(item)
        car.genRules(frequentRuleItems, minsup, minConf)
        cars.append(car, minsup, minConf)
        lastCARsNumber = currentCARsNumber
        currentCARsNumber = len(cars.rules)

    return cars