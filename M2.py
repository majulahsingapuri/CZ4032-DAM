
import sys

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
        lowest = 0
        for i in range(len(totalerrorlist)):
            if totalerrorlist[i] < totalerrorlist[lowest]:
                lowest = i
        rulelist = rulelist[:(lowest+1)]
        self.defaultclass = self.defaultclasslist[lowest]
        self.defaultclasslist = None
        self.totalerrorlist = None
    

def isRuleInDataCase(datacase,rule):
    # check if the individual data case's attribute and value the same as the precedence in rule
    for item in rule:
        if (datacase[item]!=rule[item]):
            return False
    return True
def isCorrect(datacase,rule):
    # assumption: rule must be in datacase first 
    # return if the rule correctly classify the datacase d.
    if datacase[-1]==rule.class_label:
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
    sorted(CARs)
    # highest precedence in front
    #Stage 1
    Q = set() # set of all cRules
    U = set() # 
    A = set() #collection of (dID, y, cRule, wRule)
    marked = set() # set of id of marked rules
    for id, d in enumerate(dataset):
        cRule_index=highestPrecedenceRule_correct(CARs,d)
        wRule_index=highestPrecedenceRule_wrong(CARs,d)
        if cRule_index:
            U.add(cRule_index)
            CARs[cRule_index].classCasesCovered[dataset[-1]] += 1
        if (cRule_index and wRule_index):    # if both are found
            if (CARs[cRule_index]>CARs[wRule_index]):
                Q.add(cRule_index)
                marked.add(cRule_index)
            else:
                A.add(id,d[-1],cRule_index,wRule_index)
    
    # stage 2
    for entry in A:
        if CARs[entry[3]] in marked:
            CARs[entry[2]].classCasesCovered[entry[1]] -= 1
            CARs[entry[3]].classCasesCovered[entry[1]] += 1
        else:
            wSet=allCoverRules(U, dataset[entry[0]], CARs[entry[2]], CARs)
            for w in wSet:
                CARs[w].replace.add((entry[2], entry[0], entry[1]))
                CARs[w].classCasesCovered[entry[1]] += 1
            Q=Q.union(wSet)


    # stage 3
    ruleErrors=0
    ordered_Q=sorted(list(set))
    data_cases_covered=set() 

    for r_index in ordered_Q:
        if (CARs[r_index].classCasesCovered[CARs[r_index].class_label]!=0):
            for entry in CARs[r_index].replace:
                if entry[1] in data_cases_covered:
                    CARs[r_index].classCasesCovered[entry[2]] -= 1
                else:
                    CARs[entry[0]].classCasesCovered[entry[2]] -= 1
        for i in range(len(dataset)):
            if i not in data_cases_covered:
                if isCorrect(dataset[i],CARs[r_index]) and isRuleInDataCase(dataset[i],CARs[r_index]):
                    data_cases_covered.add(i)
                    
        ruleErrors+=(errorsOfRule(CARs[r_index,],dataset))
        class_distribution=compClassDistr(dataset,data_cases_covered)
        default_class=selectDefault(class_distribution)
        defaultErrors=defErr(default_class, class_distribution)
        totolErrors=ruleErrors+defaultErrors
        classifier.add(CARs[r_index],default_class,totolErrors)
    classifier.discard()
    return classifier    







    
    
            








