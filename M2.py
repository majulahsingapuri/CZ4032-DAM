
import sys
import ruleItem
import RG

class M2:

    def __init__(self):
        self.rulelist = list()
        self.defaultclass = None
        self.defaultclasslist = list()
        self.totalerrorlist = list()

    def add(self, rule, defaultclass, totalerrors):
        self.rulelist.append(rule)
        self.defaultclasslist.append(defaultclass)
        self.totalerrorlist.append(totalerrors)

    #find first rule in C with lowest totalerrors and discard all rules after it
    def discard(self):
        lowest = self.totalerrorlist.index(min(self.totalerrorlist))
        self.rulelist = self.rulelist[:(lowest+1)]
        self.defaultclass = self.defaultclasslist[lowest]
        self.defaultclasslist = None
        self.totalerrorlist = None
    def print(self):
        for rule in self.rulelist:
            rule.print()
        print("default_class:", self.defaultclass)
    

def isRuleInDataCase(datacase,rule):
    # check if the individual data case's attribute and value the same as the precedence in rule
    for item in rule.condSet:
        if (datacase[item]!=rule.condSet[item]):
            return False
    return True
def isCorrect(datacase,rule):
    # assumption: rule must be in datacase first 
    # return if the rule correctly classify the datacase d.
    if datacase[-1]==rule.classLabel:
        return True
    else:
        return False
def highestPrecedenceRule_correct(cars,datacase):
    # return the highestPrecedenceRule
    for id,r in enumerate(cars):
        if isCorrect(datacase,r) and isRuleInDataCase(datacase,r):
            return id
    return None
def highestPrecedenceRule_wrong(cars,datacase):
    for id,r in enumerate(cars):
        if isRuleInDataCase(datacase,r) and not isCorrect(datacase,r):
            return id
    return None
def allCoverRules(U,datacase,cRule_i,cars):
    wSet=set()
    for rule_i in U:
        if cars[rule_i]>cRule_i and isRuleInDataCase(datacase,cars[rule_i]) and not isCorrect(datacase,cars[rule_i]):
            wSet.add(rule_i)
    return wSet


# how many cases that this rule classified wrongly

def errorsOfRule(r, dataset,dataCaseCovered):
    error_number = 0
    for counter,case in enumerate(dataset):
        if counter not in dataCaseCovered:
            if not isCorrect(case,r) and isRuleInDataCase(case,r):
                error_number += 1
    return error_number

def compClassDistr(dataset,dataCaseCovered):
    class_distr=dict()
    for index,datacase in enumerate(dataset):
        if index not in dataCaseCovered:
            if datacase[-1] not in class_distr:
                class_distr[datacase[-1]]=1
            else:
                class_distr[datacase[-1]]+=1

# choose the default class (majority class in remaining dataset)
def selectDefault(classDistribution):
    if classDistribution==None:
        return None
    max_key = max(classDistribution, key=classDistribution.get)
    return max_key


# count the number of errors that the default class will make in the remaining training data
def defErr(defaultClass, classDistr):
    if classDistr==None:
        return sys.maxsize
    count=0
    for className in classDistr:
        if className!=defaultClass:
            count+=classDistr[className]
    return count







def M2_classifier(CARs,dataset):
    classifier = M2()
    rule_list=list(CARs.rules)
    for i in range(len(rule_list)):
        rule_list[i]=ruleitem2rule(rule_list[i],dataset)
    sorted(rule_list)
    # highest precedence in front
    #Stage 1
    Q = set() # set of all cRules
    U = set() # 
    A = set() #collection of (dID, y, cRule, wRule)
    marked = set() # set of id of marked rules
    for id, d in enumerate(dataset):
        cRule_index=highestPrecedenceRule_correct(rule_list,d)
        wRule_index=highestPrecedenceRule_wrong(rule_list,d)
        if cRule_index:
            U.add(cRule_index)
            rule_list[cRule_index].classCasesCovered[dataset[id][-1]] += 1
        if (cRule_index and wRule_index):    # if both are found
            if (rule_list[cRule_index]>rule_list[wRule_index]):
                Q.add(cRule_index)
                marked.add(cRule_index)
            else:
                A.add((id,d[-1],cRule_index,wRule_index))
    
    # stage 2
    for entry in A:
        if rule_list[entry[3]] in marked:
            rule_list[entry[2]].classCasesCovered[entry[1]] -= 1
            rule_list[entry[3]].classCasesCovered[entry[1]] += 1
        else:
            wSet=allCoverRules(U, dataset[entry[0]], rule_list[entry[2]], rule_list)
            for w in wSet:
                rule_list[w].replace.add((entry[2], entry[0], entry[1]))
                rule_list[w].classCasesCovered[entry[1]] += 1
            Q=Q.union(wSet)


    # stage 3
    ruleErrors=0
    ordered_Q=sorted(list(Q))
    data_cases_covered=set() 

    for r_index in ordered_Q:
        if (rule_list[r_index].classCasesCovered[rule_list[r_index].classLabel]!=0):
            for entry in rule_list[r_index].replace:
                if entry[1] in data_cases_covered:
                    rule_list[r_index].classCasesCovered[entry[2]] -= 1
                else:
                    rule_list[entry[0]].classCasesCovered[entry[2]] -= 1
        for i in range(len(dataset)):
            if i not in data_cases_covered:
                if isCorrect(dataset[i],rule_list[r_index]) and isRuleInDataCase(dataset[i],rule_list[r_index]):
                    data_cases_covered.add(i)
                    
        ruleErrors+=(errorsOfRule(rule_list[r_index,],dataset))
        class_distribution=compClassDistr(dataset,data_cases_covered)
        default_class=selectDefault(class_distribution)
        defaultErrors=defErr(default_class, class_distribution)
        totolErrors=ruleErrors+defaultErrors
        classifier.add(rule_list[r_index],default_class,totolErrors)
    classifier.discard()
    return classifier    

class Rule(ruleItem.RuleItem):
    """
    classCasesCovered and replace field.
    """
    def __init__(self, cond_set, class_label, dataset):
        ruleItem.RuleItem.__init__(self, cond_set, class_label, dataset)
        self._init_classCasesCovered(dataset)
        self.replace = set()

    # initialize the classCasesCovered field
    def _init_classCasesCovered(self, dataset):
        class_column = [x[-1] for x in dataset]
        class_label = set(class_column)
        self.classCasesCovered = dict((x, 0) for x in class_label)
    
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



def ruleitem2rule(rule_item, dataset):
    rule = Rule(rule_item.condSet, rule_item.classLabel, dataset)
    return rule

if (__name__=="__main__"):

    dataset = [[1, 1, 1], [1, 1, 1], [1, 2, 1], [2, 2, 1], [2, 2, 1],
               [2, 2, 0], [2, 3, 0], [2, 3, 0], [1, 1, 0], [3, 2, 0]]
    minsup = 0.15
    minconf = 0.6
    cars=RG.rule_generator(dataset,minsup,minconf)
    classifier=M2_classifier(cars,dataset)
    classifier.print()











    
    
            








