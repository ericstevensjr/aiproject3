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

