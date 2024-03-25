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
    variableAttributes = {}
    counter = 1

    for attribute, values in attributes.items():
        for value in values:
            variableAttributes[f"{attribute}:{value}"] = counter
            counter += 1

    return variableAttributes

def constraintsPySAT(constraints, variableAttributes):
    clause = []

    for part in constraint.split('OR'):
        isNegated = 'NOT' in part
        attribute = part.replace('NOT', '').strip()
        variable = variableAttributes[attribute]
        clause.append(-variable if isNegated else variable)

    return clause

def checkFeasibility(constraints, variableAttributes):
    solver = Glucose4()

    for constraint in constraints:
        clause = constraintsPySAT(constraint, variableAttributes)
        solver.add_clause(clause)
    isSolvable = solver.solve()
    solver.delete()

    return isSolvable

def applyConstraints(encodedObjects, constraints, attributes):
    variableAttributes = assignAttributesToVariables(attributes)
    feasibleObjects = []

    for object in encodedObjects:
        if checkFeasibility(constraints, variableAttributes):
            feasibleObjects.append(object)

    return feasibleObjects

