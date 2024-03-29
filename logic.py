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
    # Assuming attributes are sorted as desired and combinations are generated accordingly
    encodedObjects = []
    for combination in combinations:
        encoded = ''.join('0' if val == attributes[attr][1] else '1' for attr, val in zip(attributes.keys(), combination))
        encodedObjects.append(encoded)
    # The encodedObjects list should now start with '000' and increment to '111'
    return encodedObjects


def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
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
    encodedObjects.reverse()
    # Generate feasibility results while preserving original order and identifiers
    feasibilityResults = [(f"o{index}", obj, isFeasible(obj, attributes, constraints)) for index, obj in enumerate(encodedObjects)]
    return feasibilityResults








def evaluateCondition(encodedObject, clause, attributes):
    # Evaluate a single condition against the encoded object
    # This function needs to be implemented based on your specific logic
    return True  # Placeholder return value

def showTable(feasibilityResults, attributes):
    print("+----------+---------------+--------------+---------------+")
    print("| encoding | fish AND wine | wine OR cake | total penalty |")
    print("+----------+---------------+--------------+---------------+")

    for idx, (objId, encodedObj, isFeasible) in enumerate(feasibilityResults):
        if isFeasible:
            # Assuming attributes are already correctly ordered and indexed
            decoded_attributes = [attributes[attr][int(bit)] for attr, bit in zip(attributes.keys(), encodedObj)]
            # Construct the row for the table; you'll need to adjust this part based on how you calculate penalties
            penalties_for_rules = ['0' for _ in range(2)]  # Placeholder for actual penalty values
            total_penalty = '0'  # Placeholder for the total penalty calculation
            row = f"| {objId.ljust(10)}| {' | '.join(penalties_for_rules).ljust(14)}| {total_penalty.ljust(13)}|"
            print(row)

    print("+----------+---------------+--------------+---------------+")


def evaluatePenaltyCondition(encodedObjects, condition, attributes, map):
    clauses = condition.split(' AND ')
    for clause in clauses:
        # Each clause can be a simple attribute or NOT attribute
        isNegated = 'NOT ' in clause
        attrValue = clause.replace('NOT ', '')
        
        # Identify the attribute and its expected binary representation
        for attribute, values in attributes.items():
            if attrValue in values:
                expected_value = map[attrValue]
                index = list(attributes.keys()).index(attribute)
                
                # Check if the condition is met in the encoded object
                actual_value = encodedObjects[index]
                if (isNegated and actual_value == expected_value) or (not isNegated and actual_value != expected_value):
                    # Clause not satisfied, return 0 penalty for this rule
                    return 0

    # If all clauses are satisfied, return the associated penalty
    return condition[1]  # Assuming the condition is a tuple (condition_str, penalty)