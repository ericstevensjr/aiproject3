import itertools

def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]
    allCombinations = itertools.product(*attributeValues)
    combinationsList = list(map(list, allCombinations))

    return combinationsList
