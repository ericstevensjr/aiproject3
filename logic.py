from pysat.solvers import Glucose4
import itertools

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

def assignAttributesToVariables(attributes):
    variableMapping = {}
    counter = 1

    for attribute, values in attributes.items():
        for value in values:
            key = f"{attribute}:{value}"
            variableMapping[key] = counter
            counter += 1

    return variableMapping

def constraintPySAT(constraint, variableMapping):
    clause = []

    for part in constraint.split('OR'):
        isNegated = 'NOT' in part
        attribute = part.replace('NOT', '').strip()
        variable = variableMapping.get(attribute, None)
        if variable:
            clause.append(-variable if isNegated else variable)

    return clause

def checkFeasibility(encodedObject, constraints, variableMapping, attributes):
    solver = Glucose4()
    objectLiterals = []

    for idx, (attribute, values) in enumerate(attributes.items()):
        bit = encodedObject[idx]
        attributeValuePair = f"{attribute}:{values[int(bit)]}"
        variable = variableMapping[attributeValuePair]
        literal = variable if bit == '1' else -variable
        objectLiterals.append(literal)

    for constraint in constraints:
        clause = constraintPySAT(constraint, variableMapping)
        solver.add_clause(clause)

    isSolvable = solver.solve(assumptions=objectLiterals)
    solver.delete()
    
    return isSolvable

def applyConstraints(encodedObjects, constraints, attributes):
    variableMapping = assignAttributesToVariables(attributes)
    feasibleObjects = []

    for object in encodedObjects:
        if checkFeasibility(object, constraints, variableMapping, attributes):
            feasibleObjects.append(object)

    return feasibleObjects

def evaluatePenaltyLogic(feasibleObjects, penaltyLogicRules, variableMapping, attributes):
    penalties = {}

    for object in feasibleObjects:
        totalPenalty = 0
        for condition, penalty in penaltyLogicRules:
            if not doesSatisfyCondition(object, condition, variableMapping, attributes):
                totalPenalty += penalty
        penalties[object] = totalPenalty

    return penalties

def evaluateQualitativeChoiceLogic(feasibleObjects, qualitativeLogicRules, variableMapping):
    preferences = []

    for object1 in feasibleObjects:
        for object2 in feasibleObjects:
            if object1 != object2:
                preference = compareObjects(object1, object2, qualitativeLogicRules, variableMapping)
                preferences.append((object1, object2, preference))

    return preferences

def compareObjects(object1, object2, qualitiativeLogicRules, variableMapping, attributes):
    preference = "incomparable"
    for rule, condition in qualitiativeLogicRules:
        if condition:
            if not doesSatisfyCondition(object1, condition, variableMapping, attributes) and not doesSatisfyCondition(object2, condition, variableMapping, attributes):
                continue

        preferred, lessPreferred = rule.split(' BT ')

        if doesSatisfyCondition(object1, preferred, variableMapping, attributes) and doesSatisfyCondition(object2, lessPreferred, variableMapping, attributes):
            preference = "object1 preferred"
        elif doesSatisfyCondition(object2, preferred, variableMapping, attributes) and doesSatisfyCondition(object1, lessPreferred, variableMapping, attributes):
            preference = "object2 preferred"

    return preference

def doesSatisfyCondition(encodedObject, condition, variableMapping, attributes):
    reverseMapping = {v: k for k, v in variableMapping.items()}

    if ':' in condition:
        attribute, value = condition.split(':')
        attributeIndex = list(attributes.keys()).index(attribute)
        expectedBit = '1' if attributes[attribute][0] == value else '0'
        return encodedObject[attributeIndex] == expectedBit
    
    return False