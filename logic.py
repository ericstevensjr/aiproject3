import itertools

def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]
    return list(itertools.product(*attributeValues))

def encodeCombinations(combinations, attributes):
    # Assuming attributes are sorted as desired and combinations are generated accordingly
    encodedObjects = []
    for combination in combinations:
        encoded = ''.join('0' if val == attributes[attr][1] else '1' for attr, val in zip(attributes.keys(), combination))
        encodedObjects.append(encoded)
    return encodedObjects

def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
        decoded_attributes = []
        for bit, (attribute, values) in zip(obj, attributes.items()):
            # Decode each bit to its corresponding attribute value
            value = values[0] if bit == '1' else values[1]
            decoded_attributes.append(value)
        print(f"o{idx}: " + ', '.join(decoded_attributes))



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

def evaluateCNF(encodedObj, cnfExpression, attributes):
    """
    Evaluates a CNF expression against an encoded object.
    
    encodedObj: Binary string representing the object.
    cnfExpression: CNF expression string.
    attributes: Ordered dict of attributes and their binary encoding positions.
    """
    # Mapping attribute names to their positions and binary values
    attr_positions = {attr: i for i, attr in enumerate(attributes)}
    
    # Split CNF into individual clauses
    clauses = cnfExpression.split(" AND ")
    for clause in clauses:
        # Initialize clause evaluation as False
        clause_eval = False
        
        literals = clause.split(" OR ")
        for literal in literals:
            negated = "NOT " in literal
            literal_attr = literal.replace("NOT ", "")
            
            # Determine the attribute and its expected binary value for the literal
            for attr, values in attributes.items():
                if literal_attr in values:
                    pos = attr_positions[attr]
                    expected_val = '0' if values.index(literal_attr) else '1'
                    if negated:
                        expected_val = '1' if expected_val == '0' else '0'
                    
                    # Check if the literal evaluates to True
                    if encodedObj[pos] == expected_val:
                        clause_eval = True
                        break

        # If any clause is not satisfied, return True to indicate penalty applies
        if not clause_eval:
            return True
    
    # All clauses are satisfied, return False indicating no penalty
    return False

def applyPenalties(feasibleObjects, penaltyLogicRules, attributes):
    penalties_summary = []

    for objId, encodedObj, _ in feasibleObjects:
        penalties = []
        for cnfExpression, penalty in penaltyLogicRules:
            # If the CNF expression is not satisfied, apply the penalty
            if evaluateCNF(encodedObj, cnfExpression, attributes):
                penalties.append(penalty)
            else:
                penalties.append(0)
        total_penalty = sum(penalties)
        penalties_summary.append((objId, penalties, total_penalty))
    
    return penalties_summary

def showTable(feasibleObjects, penaltyLogicRules, attributes):
    print("+----------+---------------+--------------+---------------+")
    print("| encoding | fish AND wine | wine OR cake | total penalty |")
    print("+----------+---------------+--------------+---------------+")
    
    # Filter out infeasible objects
    feasibleObjects = [(objId, encodedObj, isFeasible) for objId, encodedObj, isFeasible in feasibleObjects if isFeasible]

    penalties_summary = applyPenalties(feasibleObjects, penaltyLogicRules, attributes)
    for objId, penalties, total_penalty in penalties_summary:
        penalties_str = " | ".join(str(p).ljust(14) for p in penalties)
        print(f"| {objId.ljust(10)}| {penalties_str}| {str(total_penalty).ljust(13)}|")
    print("+----------+---------------+--------------+---------------+")

def evaluateCNF(encodedObj, cnfExpression, attributes):
    attrToIndex = {attr: idx for idx, attr in enumerate(attributes)}
    for clause in cnfExpression.split(" AND "):
        clauseSatisfied = False
        for literal in clause.split(" OR "):
            negated = literal.startswith("NOT ")
            literalAttr = literal.replace("NOT ", "")
            for attr, values in attributes.items():
                if literalAttr in values:
                    idx = attrToIndex[attr]
                    expectedValue = '0' if negated else '1'
                    if encodedObj[idx] == expectedValue:
                        clauseSatisfied = True
                        break
        if not clauseSatisfied:
            return True  # Clause not satisfied, so penalty applies
    return False  # All clauses satisfied, so no penalty



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