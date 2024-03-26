import itertools

def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]
    allCombinations = itertools.product(*attributeValues)
    combinationsList = list(map(list, allCombinations))

    return combinationsList


def encodeCombinations(combinations, attributes):
    valuePositions = {attribute: {value: idx for idx, value in enumerate(values)} for attribute, values in attributes.items()}
    encodedObjects = []

    for combination in combinations:
        encodedObject = ''

        for attribute, value in zip(attributes.keys(), combination):
            bit = '1' if valuePositions[attribute][value] == 0 else '0'
            encodedObject += bit
        encodedObjects.append(encodedObject)

    return encodedObjects

def mapAttributesToIntegers(attributes):
    map = {}
    reversedMap = {}
    counter = 1

    for attribute, values in attributes.items():
        for value in values:
            map[f"{attribute}:{value}"] = counter
            reversedMap[counter] = f"{attribute}:{value}"
            counter += 1

    return map, reversedMap


def convertConstraintsToClauses(constraints, map):
    clauses = []

    for constraint in constraints:
        clause = []
        
        for literal in constraints:
            if "NOT" in literal:
                attributeValue = literal.repalce("NOT ", "").strip()
                clause.append(-map[attributeValue])
            else:
                clause.append(map[literal])
        clauses.append(clause)

    return clauses