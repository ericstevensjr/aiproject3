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
    print("Inside isFeasible, attributes is a:", type(attributes))
    # Maps attribute names to their indexes based on the ordering in attributes
    attribIndex = {attrib: i for i, attrib in enumerate(attributes.keys())}

    for constraint in constraints:
        clauseSatisfied = False
        for literal in constraint:
            isNegated = 'NOT ' in literal
            # Extract attribute name and value from the literal
            attributeValue = literal.replace('NOT ', '').strip()
            for attribute, values in attributes.items():
                if attributeValue in values:
                    # Determine the index of the attribute in the encoded object
                    index = attribIndex[attribute]
                    # Determine the expected bit value based on whether the literal is negated
                    expectedBit = '0' if isNegated else '1'
                    # Determine the bit value in the encoded object
                    actualBit = encodedObject[index]
                    if actualBit == expectedBit:
                        clauseSatisfied = True
                        break  # A single true literal is enough for the clause to be satisfied
            if clauseSatisfied:
                break  # Move to the next clause if the current one is satisfied

        if not clauseSatisfied:
            # If after checking all literals in a clause, none are satisfied, the object is infeasible
            return False

    # The object is feasible if all clauses are either satisfied or at least one literal per clause is satisfied
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
