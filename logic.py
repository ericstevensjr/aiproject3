import itertools
from pysat.solvers import Glucose4

def generateCombinations(attributes):
    # Extracting attribute values and generating all possible combinations
    attributeValues = [values for values in attributes.values()]
    allCombinations = itertools.product(*attributeValues)
    
    return list(allCombinations)


def encodeCombinations(combinations, attributes):
    # Mapping each attribute value to its binary representation
    valuePositions = {attribute: {value: idx for idx, value in enumerate(values)} for attribute, values in attributes.items()}
    encodedObjects = []

    for combination in combinations:
        encodedObject = ''
        for attribute, value in zip(attributes.keys(), combination):
            # Encoding the first value as '1' and the second as '0'
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


def convertConstraintsToClauses(constraints, mapping):
    clauses = []
    for constraint in constraints:
        clause = []
        for literal in constraint:
            # Assume literals are now correctly prefixed with attribute names, e.g., "drink:wine"
            negated = 'NOT ' in literal
            cleaned_literal = literal.replace("NOT ", "").strip()
            
            if cleaned_literal in mapping:  # Direct lookup if literal is correctly formed
                mappedValue = mapping[cleaned_literal]
                clause.append(-mappedValue if negated else mappedValue)
            else:
                print(f"Warning: '{cleaned_literal}' not found in mapping.")
        clauses.append(clause)
    return clauses


def checkFeasibility(clauses):
    solver = Glucose4()

    for clause in clauses:
        solver.add_clause(clause)
    isSatisfiable = solver.solve()
    solver.delete()

    return isSatisfiable


def evaluateCNF(condition, encodedObject, encodingMap):
    clauses = condition.split(' AND ')

    for clause in clauses:
        clause = clause.strip()
        literals = clause.split(' OR ')
        clauseSatisfied = False

        for literal in literals:
            negated = 'NOT' in literal
            if negated:
                attributeValue = literal.replace("NOT ", "").strip()
            else:
                attributeValue = literal.strip()
            literal = literal.strip()
            attribute, value = literal.split(':')
            
            if attributeValue in encodingMap:
                index = encodingMap[attributeValue]
                expectedValue = '0' if negated else '1'

                if encodedObject[index] == expectedValue:
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


def createEncodingMapping(attributes):
    encodingMap = {}

    for idx, (attribute, values) in enumerate(attributes.items()):
        for value in values:
            encodingMap[f"{attribute}:{value}"] = idx
        
    return encodingMap


def compareObjectsUsingQCL(object1, object2, qualitativeLogicRules, map):
    for preferences, condition in qualitativeLogicRules:
        if condition and (not evaluateCNF(condition, object1, map) or not evaluateCNF(condition, object2, map)):
            continue

        preferenceResult = evaluatePreferences(object1, object2, preferences, map)

        if preferenceResult != "incomparable":
            return preferenceResult
        
    return "incomparable"


def evaluatePreferences(object1, object2, preferences, map):
    for preference in preferences:
        attribute1, value1, attribute2, value2 = parsePreference(preference)
        position1 = map[f"{attribute1}:{value1}"]
        position2 = map[f"{attribute2}:{value2}"]

        bit1 = object1[position1] == '1'
        bit2 = object2[position2] == '1'

        if bit1 and not bit2:
            return "object1 preferred over object2"
        elif not bit1 and bit2:
            return "object2 preferred over object1"

    return "incomparable"

def parsePreference(preference):
    parts = preference.split('BT')

    if len(parts) != 2:
        raise ValueError(f"Invalid preference format: {preference}")
    
    attributeValuePair1 = parts[0].strip()
    attributeValuePair2 = parts[1].strip()
    attribute1, value1 = attributeValuePair1.split(':')
    attribute2, value2 = attributeValuePair2.split(':')

    return attribute1.strip(), value1.strip(), attribute2.strip(), value2.strip()