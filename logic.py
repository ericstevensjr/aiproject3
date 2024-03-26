import itertools
from pysat.solvers import Glucose4

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

        for literal in constraint:
            if "NOT" in literal:
                attributeValue = literal.replace("NOT ", "").strip()
                clause.append(-map[attributeValue])
            else:
                clause.append(map[literal])
        clauses.append(clause)

    return clauses


def checkFeasibility(clauses):
    solver = Glucose4()

    for clause in clauses:
        solver.add_clause(clause)
    isSatisfiable = solver.solve()
    solver.delete()

    return isSatisfiable


def evaluateCNF(condition, encodedObject, map):
    clauses = condition.split('AND')

    for clause in clauses:
        clause = clause.strip()
        literals = clause.split('OR')
        clauseSatisfied = False

        for literal in literals:
            literal = literal.strip()
            attribute, value = literal.split(':')
            
            if encodedObject[map[attribute + ':' + value]] == 1:
                clauseSatisfied = True
                break
        if not clauseSatisfied:
            return False
        
    return True


def calculatePenalties(feasbileObjects, penaltyLogicRules, map):
    objectPenalties = {}

    for encodedObject in feasbileObjects:
        totalPenalty = 0

        for condition, penalty in penaltyLogicRules:
            if evaluateCNF(condition, encodedObject, map):
                totalPenalty += penalty
        objectPenalties[encodedObject] = totalPenalty
    
    return objectPenalties