from pysat.solvers import Glucose4
import itertools

def assignAttributesToVariables(attributes):
    variableMap = {}
    counter = 1

    for attribute, values in attributes.items():
        for value in values:
            key = f"{attribute}:{value}"
            variableMap[key] = counter
            counter += 1

    return variableMap

def encodeConstraints(constraints, variableMap):
    encodedConstraints = []

    for constraint in constraints:
        clause = []

        for literal in constraint:
            isNegated = 'NOT in literal'
            attributeValue = literal.repalce('NOT ', '')
            variable = variableMap[attributeValue]
            clause.append(-variable if isNegated else variable)
        encodeConstraints.append(clause)

    return encodeConstraints