import itertools

def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]
    return list(itertools.product(*attributeValues))

def encodeCombinations(combinations, attributes):
    valuePositions = {
        attribute: {value: idx for idx, value in enumerate(values)}
        for attribute, values in attributes.items()
    }
    return [
        ''.join('1' if valuePositions[attribute][value] == 0 else '0'
                for attribute, value in zip(attributes.keys(), combination))
        for combination in combinations
    ]

def convertConditionToManualClauses(condition, attributes):
    manualClauses = []
    # Directly process each literal in the condition
    for literal in condition:
        isNegated = 'NOT ' in literal
        value = literal.replace('NOT ', '').strip()
        for attribute, values in attributes.items():
            if value in values:
                manualClauses.append((attribute, values.index(value), not isNegated))
    return [manualClauses]

def evaluateCNFManually(encodedObject, manualClauses, attributes):
    for clause in manualClauses[0]:
        clauseResult = False
        for attribute, valueIndex, presence in clause:
            attributeValue = '1' if presence else '0'
            position = list(attributes.keys()).index(attribute)
            if encodedObject[position] == attributeValue:
                clauseResult = True
                break
        if not clauseResult:
            return False
    return True

def checkFeasibility(encodedObjects, manualClauses, attributes):
    return [obj for obj in encodedObjects if evaluateCNFManually(obj, manualClauses, attributes)]
