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
    encodedObjects = []
    for combination in combinations:
        encodedObject = ''
        for value, (attribute, values) in zip(combination, attributes.items()):
            # Assign '1' for the first listed value and '0' for the second listed value
            bit = '1' if values.index(value) == 0 else '0'
            encodedObject += bit
        encodedObjects.append(encodedObject)
    return encodedObjects

def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(reversed(encodedObjects)):
        decoded_attributes = []
        for bit, (attribute, values) in zip(obj, attributes.items()):
            # Decode each bit to its corresponding attribute value
            value = values[0] if bit == '1' else values[1]
            decoded_attributes.append(value)
        print(f"o{idx} – {obj}: " + ', '.join(decoded_attributes))



def isFeasible(encodedObject, attributes, constraints):
    # Convert attributes to a list to ensure consistent ordering
    attributesList = list(attributes.keys())

    for constraint in constraints:
        # Start with the assumption that the clause is not satisfied
        clauseSatisfied = False

        for literal in constraint:
            isNegated = 'NOT ' in literal
            attributeValue = literal.replace('NOT ', '')

            # Determine which attribute and value this literal corresponds to
            for attribute, values in attributes.items():
                if attributeValue in values:
                    attributeIndex = attributesList.index(attribute)
                    valueIndex = values.index(attributeValue)
                    bit = '1' if valueIndex == 0 else '0'

                    if isNegated:
                        # For negation, the clause is satisfied if the bit is NOT set
                        if encodedObject[attributeIndex] != bit:
                            clauseSatisfied = True
                            break
                    else:
                        # For a regular literal, the clause is satisfied if the bit is set
                        if encodedObject[attributeIndex] == bit:
                            clauseSatisfied = True
                            break

        # If none of the literals in a clause are satisfied, the object is infeasible
        if not clauseSatisfied:
            return False

    # The object is feasible if it does not violate any of the constraints
    return True


def checkFeasibility(encodedObjects, attributes, constraints):
    # Assuming constraints are properly formatted
    print("Correcting call to isFeasible with actual attributes:", attributes)
    feasibleObjects = [obj for obj in encodedObjects if isFeasible(obj, attributes, constraints)]
    return feasibleObjects



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
