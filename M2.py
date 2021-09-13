


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

class M2_classifier(CARs,dataset):
    sorted(CARs)
    


