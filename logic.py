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
        part = part.replace('NOT ', '').strip()
        for key, var in variableMapping.items():
            if part in key:
                if isNegated:
                    var = -var
                clause.append(var)
                break
    return clause

def checkFeasibility(encodedObject, constraints, variableMapping, attributes):
    solver = Glucose4()
    objectLiterals = []
    clause = []

    for key, _ in variableMapping.items():
        if ":" not in key:
            continue  # Skip this iteration if the key format is not correct
        attribute, value = key.split(":")

        for constraint in constraints:
            clause = []
            parts = constraint.split('OR')
            for part in parts:
                part = part.strip()
                negated = 'NOT ' in part
                part_cleaned = part.replace('NOT ', '').strip()
                pass

                for attribute, values in attributes.items():  # Ensure values are iterable
                    if part_cleaned in values:  # Correctly check if part_cleaned is one of the attribute's values
                        key = f"{attribute}:{part_cleaned}"
                        variable = variableMapping.get(key, None)
                        if variable is not None:
                            clause.append(-variable if negated else variable)
                            break
            if clause:
                solver.add_clause(clause)
                pass
    
        print(f"Checking object: {encodedObject}, with clauses: {clause}, and assumptions: {objectLiterals}")

    isSolvable = solver.solve(assumptions=objectLiterals)

    return isSolvable

def applyConstraints(encodedObjects, constraints, attributes, variableMapping):
    feasibleObjects = []

    for object in encodedObjects:
        if checkFeasibility(object, constraints, variableMapping, attributes):
            feasibleObjects.append(object)
            

    return feasibleObjects

def evaluatePenaltyLogic(feasibleObjects, penaltyLogicRules, attributes):
    penalties = {}
    for obj in feasibleObjects:
        totalPenalty = 0
        for condition, penalty in penaltyLogicRules:
            # Debugging print to check condition evaluation and penalty application
            isConditionMet = interpretAndCheckCondition(obj, condition, attributes)
            if isConditionMet:
                totalPenalty += penalty
        penalties[obj] = totalPenalty
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

def interpretAndCheckCondition(encodedObject, condition, attributes):
    # This function will interpret conditions like 'fish AND wine' or 'wine OR cake'
    # against the encoded representation of objects.
    
    # Split the condition on 'AND' and 'OR' to handle compound conditions
    and_conditions = condition.split(' AND ')
    for and_cond in and_conditions:
        or_conditions = and_cond.split(' OR ')
        # For OR conditions, if any condition is true, the OR condition is met.
        if not any(checkConditionPart(encodedObject, part.strip(), attributes) for part in or_conditions):
            return False
    return True

def checkConditionPart(encodedObject, part, attributes):
    attribute_order = list(attributes.keys())
    # Determine the expected value ('1' or '0') for this part of the condition
    for i, attr in enumerate(attribute_order):
        if part.startswith('NOT '):
            part = part[4:]
            if part in attributes[attr]:
                return encodedObject[i] == '0'  # Inverted logic for NOT
        else:
            if part in attributes[attr]:
                return encodedObject[i] == '1'
    return False

def evaluateOrCondition(cond, encodedObject, attributes):
    # This function evaluates a condition that might contain an OR, e.g., "wine OR cake"
    attribute, value = splitCondition(cond, attributes)
    if attribute in attributes and value in attributes[attribute]:
        attr_index = list(attributes.keys()).index(attribute)
        expected_value = '1' if attributes[attribute][0] == value else '0'
        return encodedObject[attr_index] == expected_value
    return False

def evaluateCondition(encodedObject, condition, attributes):
    attribute_order = list(attributes.keys())
    condition_parts = condition.split(' AND ')
    for part in condition_parts:
        if ' OR ' in part:
            # Split the part on 'OR' and check if any subpart is true
            if not any(subpart.strip() in encodedObject for subpart in part.split('OR')):
                return False
        else:
            attribute, value = part.split(':')
            index = attribute_order.index(attribute)
            expected = '1' if attributes[attribute][0] == value else '0'
            if encodedObject[index] != expected:
                return False
    return True

def splitCondition(cond, attributes):
    # Helper function to extract attribute and value from a condition string
    for attribute in attributes.keys():
        if attribute in cond:
            if 'NOT' in cond:
                value = cond.replace('NOT ', '').replace(attribute, '').strip()
            else:
                value = cond.replace(attribute, '').strip()
            return attribute, value
    return None, None


def checkLiteral(literal, encodedObject, attributes, variableMapping):
    isNegated = 'NOT' in literal
    attr_val = literal.replace('NOT ', '').strip()
    for key, value in variableMapping.items():
        if key.endswith(attr_val):
            attribute = key.split(':')[0]
            attrIndex = list(attributes.keys()).index(attribute)
            encodedVal = '1' if attributes[attribute][0] in key else '0'
            if isNegated:
                return encodedObject[attrIndex] != encodedVal
            else:
                return encodedObject[attrIndex] == encodedVal
    return False

def evaluateSingleCondition(condition, encodedObject, attribute_order, attributes):
    negated = 'NOT' in condition
    if negated:
        condition = condition.replace('NOT ', '')

    attribute, value = None, None
    for attr, vals in attributes.items():
        if condition in vals:
            attribute = attr
            value = condition
            break

    if attribute is None:
        return False

    attribute_index = attribute_order.index(attribute)
    encoded_value = '1' if attributes[attribute][0] == value else '0'
    if negated:
        return encodedObject[attribute_index] != encoded_value
    else:
        return encodedObject[attribute_index] == encoded_value
    
def evaluateConditionComponent(component, encodedObject, attributes):
    # This function needs to determine if 'component' is an attribute or a value of an attribute
    for attribute, values in attributes.items():
        if component in values:  # If the component is a value of this attribute
            attributeIndex = list(attributes.keys()).index(attribute)  # Find the attribute's index
            expectedBit = '1' if values.index(component) == 0 else '0'  # Assuming first value corresponds to '1'
            return encodedObject[attributeIndex] == expectedBit
    return False  # If the component doesn't match any attribute value