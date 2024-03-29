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

def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
        decoded_attributes = []
        # Iterate over each bit in the encoded object and the corresponding attribute simultaneously
        for bit, (attribute, values) in zip(obj, attributes.items()):
            # The bit determines the index of the selected value (0 or 1)
            value = values[int(bit)]
            decoded_attributes.append(value)
        print(f"o{idx} – " + ', '.join(decoded_attributes))


def checkFeasibility(encodedObjects, manualClauses, attributes):
    # This is a placeholder; your implementation will vary based on how you plan to evaluate feasibility
    feasibleObjects = []
    for obj in encodedObjects:
        if all(evaluateCondition(obj, clause, attributes) for clause in manualClauses):
            feasibleObjects.append(obj)
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
