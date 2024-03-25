import itertools

def parseAttributesFile(filepath):
    attributes = {} 

    with open(filepath, 'r') as attributesFile:
        for line in attributesFile:
            attribute, valuesString = line.strip().split(':')
            values = [value.strip() for value in valuesString.split(',')]  
            attributes[attribute.strip()] = values  
    return attributes

def parseConstraintsFile(filepath):
    constraints = []

    with open(filepath, 'r') as constraintsFile:
        for line in constraintsFile:
            constraint = line.strip()
            constraints.append(constraint)
    return constraints

def parsePenaltyLogicFile(filepath):
    penaltyLogicRules = []

    with open(filepath, 'r') as file:
        for line in file:
            condition, penalty = line.strip().split(',')
            penaltyLogicRules.append((condition.strip(), int(penalty.strip())))
    return penaltyLogicRules

def parseQualitiativeLogicFile(filepath):
    qualitiativeLogicRules = []

    with open(filepath, 'r') as file:
        for line in file:
            separateParts = line.strip().split('IF')
            rule = separateParts[0].strip
            condition = separateParts[1].strip() if len(separateParts) > 1 else ""
            qualitiativeLogicRules.append((rule, condition))
    return qualitiativeLogicRules

def generateEncodedObjects(attributes):
    values = list(attributes.values())
    combinations = list(itertools.product(*values))

    encodedObjects = []
    for combination in combinations:
        encodedObj = ''
        for attribute, value in zip(attributes.keys(), combination):
            encodedObj += '1' if value == attributes[attribute][0] else '0'
        encodedObjects.append(encodedObj)
    return encodedObjects

def applyConstraints(objects, constraints):
    feasibleObjects = []

    for object in objects:
        isFeasible = True
        for constraint in constraints:
            if not evaluateConstraint(object, constraint):
                isFeasible = False
        
        if isFeasible:
            feasibleObjects.append(object)
    
    return feasibleObjects