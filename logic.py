import itertools

def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]
    return list(itertools.product(*attributeValues))

def encodeCombinations(combinations, attributes):
    valuePositions = {
        attribute: {value: idx for idx, value in enumerate(values)}
        for attribute, values in attributes.items()
    }
    return [
        ''.join('1' if valuePositions[attribute][value] == 0 else '0'
                for attribute, value in zip(attributes.keys(), combination))
        for combination in combinations
    ]

def encodeCombinations(combinations, attributes):
    """
    Encodes each combination of attribute values into binary strings where
    the first listed value gets a '1' and the second listed value gets a '0'.
    """
    encodedObjects = []
    for combination in combinations:
        encodedObject = ''
        for value, (attribute, values) in zip(combination, attributes.items()):
            # Assign '1' for the first listed value and '0' for the second
            bit = '1' if values.index(value) == 0 else '0'
            encodedObject += bit
        encodedObjects.append(encodedObject)
    return encodedObjects

def performEncoding(encodedObjects, attributes):
    """
    Prints the encoded objects along with their decoded attribute values.
    Adjusted to ensure the binary encoding reflects the new scheme.
    """
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
        decoded_attributes = []
        for bit, (attribute, values) in zip(obj, attributes.items()):
            # Decode each bit to its corresponding attribute value
            value = values[0] if bit == '1' else values[1]
            decoded_attributes.append(value)
        print(f"o{idx} – " + ', '.join(decoded_attributes))




def isFeasible(encodedObject, constraints, attributes):
    """
    Check if an encoded object satisfies all the given CNF constraints.

    :param encodedObject: A string representing an object's encoded binary attributes.
    :param constraints: A list of lists, where each sub-list represents a disjunction of literals (attribute-value pairs) that form a clause.
    :param attributes: Dictionary of attributes and their possible values to map encoded positions back to attribute values.
    :return: Boolean indicating if the object is feasible (True) or not (False).
    """
    for clause in constraints:
        clauseSatisfied = False
        for literal in clause:
            negated = 'NOT ' in literal
            attributeValue = literal.replace('NOT ', '')
            
            # Find which attribute this literal refers to, and its index (0 or 1)
            for attribute, values in attributes.items():
                if attributeValue in values:
                    attributeIndex = list(attributes).index(attribute)
                    valueIndex = values.index(attributeValue)
                    encodedValue = int(encodedObject[attributeIndex])
                    
                    # Check if the literal is satisfied
                    if (negated and encodedValue != valueIndex) or (not negated and encodedValue == valueIndex):
                        clauseSatisfied = True
                        break  # A single satisfied literal is enough for the clause

        if not clauseSatisfied:
            return False  # If any clause is not satisfied, the object is not feasible

    return True  # All clauses satisfied

def checkFeasibility(encodedObjects, constraints, attributes):
    """
    Filters the encoded objects based on their feasibility against given constraints.

    :param encodedObjects: List of strings, each representing an object's encoded attributes.
    :param constraints: A list of lists representing the CNF constraints.
    :param attributes: Dictionary of attributes and their possible values for decoding.
    :return: List of feasible encoded objects.
    """
    return [obj for obj in encodedObjects if isFeasible(obj, constraints, attributes)]

def evaluateCondition(encodedObject, clause, attributes):
    # Evaluate a single condition against the encoded object
    # This function needs to be implemented based on your specific logic
    return True  # Placeholder return value

def showTable(feasibleObjects, penaltyLogicRules, attributes):
    print("+----------+---------------+--------------+---------------+")
    print("| encoding | fish AND wine | wine OR cake | total penalty |")
    print("+----------+---------------+--------------+---------------+")

    for idx, obj in enumerate(feasibleObjects):
        penalties_for_rules = []
        total_penalty = 0
        for condition, penalty in penaltyLogicRules:
            # This assumes you have a function to evaluate a penalty rule's condition against an object
            if evaluatePenaltyCondition(obj, condition, attributes):
                total_penalty += penalty
                penalties_for_rules.append(penalty)
            else:
                penalties_for_rules.append(0)
        penalties_display = ' | '.join(str(p) for p in penalties_for_rules)
        print(f"| o{idx:<8}| {penalties_display} | {total_penalty:<13}|")
    print("+----------+---------------+--------------+---------------+")

def evaluatePenaltyCondition(encodedObject, condition, attributes):
    # Evaluate a penalty condition against the encoded object
    # Placeholder for actual implementation
    return True
