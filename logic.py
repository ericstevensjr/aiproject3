from pysat.solvers import Glucose4
import itertools

def generateEncodedObjects(attributes):
    # Generate all possible combinations of attribute values
    values_combinations = list(itertools.product(*attributes.values()))
    encoded_objects = []

    for combination in values_combinations:
        encoded = ''.join('1' if value == attributes[attribute][0] else '0' 
                          for attribute, value in zip(attributes.keys(), combination))
        encoded_objects.append(encoded)
    
    return encoded_objects

def mappingAttributesToVariables(attributes):
    variableMapping = {}
    reverse_mapping = {}  # Optional: For easy lookup in interpretations
    counter = 1

    for attribute, values in attributes.items():
        for value in values:
            key = f"{attribute}:{value}"
            variableMapping[key] = counter
            reverse_mapping[counter] = key  # Reverse mapping
            counter += 1

    return variableMapping, reverse_mapping  # Return both mappings if reverse mapping is needed

def applyConstraints(encodedObjects, constraints, variableMapping, attributes):
    solver = Glucose4()

    for constraint in constraints:
        clause = []
        for literal in constraint.replace('NOT ', '-').split('OR'):
            # Clean up and identify if literal is negated
            is_negated, *literal_parts = literal.strip().split(' ')
            literal = ''.join(literal_parts)

            if literal in variableMapping:
                # Prepend '-' for negated literals to comply with PySAT format
                variable = f"-{variableMapping[literal]}" if 'NOT' in is_negated else str(variableMapping[literal])
                clause.append(int(variable))

        if clause:
            solver.add_clause(clause)

    is_solvable = solver.solve()
    solver.delete()  # Important to free resources after solving
    return is_solvable

def evaluatePenaltyLogic(feasibleObjects, penaltyLogicRules, attributes, variableMapping):
    penalties = {}
    for obj in feasibleObjects:
        totalPenalty = 0
        for condition, penalty in penaltyLogicRules:
            if evaluateCondition(obj, condition, attributes, variableMapping):
                totalPenalty += penalty
        penalties[obj] = totalPenalty
    return penalties

def evaluateCondition(encodedObject, condition, attributes, variableMapping):
    # Split condition into individual clauses (assuming AND logic between clauses)
    clauses = condition.split('AND')
    for clause in clauses:
        # Each clause can be a single literal or multiple literals with OR logic
        if not evaluateOrClause(clause.strip(), encodedObject, attributes, variableMapping):
            return False
    return True

def evaluateOrClause(clause, encodedObject, attributes, variableMapping):
    literals = clause.split('OR')
    for literal in literals:
        if evaluateLiteral(literal.strip(), encodedObject, attributes, variableMapping):
            return True  # If any literal is True, the OR clause is True
    return False  # None of the literals in the OR clause is True

def evaluateLiteral(literal, encodedObject, attributes, variableMapping):
    isNegated = 'NOT' in literal
    literal = literal.replace('NOT ', '').strip()
    attribute, value = next((attr, val) for attr, val in variableMapping if literal in attr)

    attrIndex = list(attributes.keys()).index(attribute)
    expectedValue = '1' if attributes[attribute][0] == value else '0'
    actualValue = encodedObject[attrIndex]

    return (actualValue == expectedValue) != isNegated

def evaluateQualitativeChoiceLogic(feasibleObjects, qualitativeLogicRules, attributes, variableMapping):
    preferences = {}
    for obj1 in feasibleObjects:
        for obj2 in feasibleObjects:
            if obj1 == obj2:
                continue  # Skip comparison with itself
            preference = compareObjects(obj1, obj2, qualitativeLogicRules, attributes, variableMapping)
            preferences[(obj1, obj2)] = preference
    return preferences

def compareObjects(obj1, obj2, qualitativeLogicRules, attributes, variableMapping):
    for rule, condition in qualitativeLogicRules:
        if not evaluateCondition(condition, attributes, variableMapping):
            continue  # Skip rules whose conditions are not met
        preference = evaluateRule(rule, obj1, obj2, attributes, variableMapping)
        if preference:
            return preference
    return "incomparable"  # Default if no rules apply

def evaluateRule(rule, obj1, obj2, attributes, variableMapping):
    preferenceParts = rule.split('BT')
    for i in range(len(preferenceParts) - 1):
        preferredCondition = preferenceParts[i].strip()
        lessPreferredCondition = preferenceParts[i + 1].strip()
        
        if evaluateCondition(obj1, preferredCondition, attributes, variableMapping) and evaluateCondition(obj2, lessPreferredCondition, attributes, variableMapping):
            return "obj1 preferred over obj2"
        elif evaluateCondition(obj2, preferredCondition, attributes, variableMapping) and evaluateCondition(obj1, lessPreferredCondition, attributes, variableMapping):
            return "obj2 preferred over obj1"
    return None  # No preference determined by this rule

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