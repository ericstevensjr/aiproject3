import itertools
from pysat.solvers import Glucose4

def generateCombinations(attributes):
    # Extracting attribute values and generating all possible combinations
    attributeValues = [values for values in attributes.values()]
    allCombinations = itertools.product(*attributeValues)
    
    return list(allCombinations)


def encodeCombinations(combinations, attributes):
    # Mapping each attribute value to its binary representation
    valuePositions = {attribute: {value: idx for idx, value in enumerate(values)} for attribute, values in attributes.items()}
    encodedObjects = []

    for combination in combinations:
        encodedObject = ''
        for attribute, value in zip(attributes.keys(), combination):
            # Encoding the first value as '1' and the second as '0'
            bit = '1' if valuePositions[attribute][value] == 0 else '0'
            encodedObject += bit
        encodedObjects.append(encodedObject)

    print("Encoded Objects:", encodedObjects)  # Print statement added
    return encodedObjects


def mapAttributesToIntegers(attributes):
    mapping = {}
    reverseMapping = {}
    counter = 1  # Start counter at 1 since PySAT uses positive and negative integers

    for attribute, values in attributes.items():
        for value in values:
            mapping[f"{attribute}:{value}"] = counter
            reverseMapping[counter] = f"{attribute}:{value}"
            counter += 1

    print("Mapping:", mapping)  # Print statement added
    print("Reverse Mapping:", reverseMapping)  # Print statement added
    return mapping, reverseMapping


def convertConstraintsToClauses(constraints, attributes, mapping):
    clauses = []
    for constraint in constraints:
        clause = []
        for literal in constraint:
            isNegated = 'NOT ' in literal
            value = literal.replace('NOT ', '').strip() if isNegated else literal.strip()

            # Find the attribute that this value belongs to
            found = False
            for attribute, values in attributes.items():
                if value in values:
                    # Correctly construct the key for the mapping
                    key = f"{attribute}:{value}"
                    if isNegated:
                        clause.append(-mapping[key])
                    else:
                        clause.append(mapping[key])
                    found = True
                    break
            
            if not found:
                print(f"Warning: {value} not found in mapping.")
                
        if clause:  # Ensure we don't add empty clauses
            clauses.append(clause)
    return clauses

def checkFeasibility(clauses):
    solver = Glucose4()
    for clause in clauses:
        solver.add_clause(clause)
    isFeasible = solver.solve()
    solver.delete()  # Clean up the solver instance
    return isFeasible

def inferAttributeFromValue(value, attributes):
    for attribute, values in attributes.items():
        if value in values:
            return attribute
    return None


def evaluateCNF(cnfCondition, encodedObject, attributes):
    clauses = cnfCondition.split(' AND ')
    
    for clause in clauses:
        clauseSatisfied = False
        literals = clause.split(' OR ')
        
        for literal in literals:
            negated = 'NOT' in literal
            value = literal.replace('NOT ', '').strip() if negated else literal.strip()
            
            # Infer the attribute for the given value
            attribute = inferAttributeFromValue(value, attributes)
            if not attribute:
                print(f"Attribute not found for value: {value}")
                return False
            
            attrIndex = list(attributes.keys()).index(attribute)
            valueIndex = attributes[attribute].index(value)
            
            # Determine expected and actual values
            expectedValue = '0' if negated else '1'
            actualValue = '1' if valueIndex == 0 else '0'
            
            if encodedObject[attrIndex] == expectedValue:
                clauseSatisfied = True
                break
        
        if not clauseSatisfied:
            return False
            
    return True




def calculatePenalties(feasibleObjects, penaltyLogicRules, attributes):
    objectPenalties = {}

    for encodedObject in feasibleObjects:
        totalPenalty = 0
        for condition, penalty in penaltyLogicRules:
            if evaluateCNF(condition, encodedObject, attributes):
                totalPenalty += penalty
        objectPenalties[encodedObject] = totalPenalty

    return objectPenalties



def createEncodingMapping(attributes):
    encodingMap = {}

    for idx, (attribute, values) in enumerate(attributes.items()):
        for value in values:
            encodingMap[f"{attribute}:{value}"] = idx
        
    return encodingMap


def compareObjectsUsingQCL(object1, object2, qualitativeLogicRules, attributesMapping):
    for rule in qualitativeLogicRules:
        preferences, condition = rule
        # Check condition, if present
        if condition and not evaluateCNF(condition, object1, attributesMapping) and not evaluateCNF(condition, object2, attributesMapping):
            continue  # Skip this rule if the condition is not met by either object
        
        # Evaluate preferences
        result = evaluatePreferences(preferences, object1, object2, attributesMapping)
        if result != 'incomparable':
            return result  # Return the result if a preference is determined
    
    return 'incomparable'  # Return 'incomparable' if no preferences determined


def evaluatePreferences(preferences, object1, object2, mapping):
    preferenceParts = preferences.split('BT')
    if len(preferenceParts) != 2:
        print("Warning: Invalid preference format.")
        return 'incomparable'
    
    pref1, pref2 = preferenceParts
    pref1 = pref1.strip()
    pref2 = pref2.strip()

    # Assuming preferences are specified as "attribute:value"
    index1 = mapping.get(pref1, -1)
    index2 = mapping.get(pref2, -1)

    if index1 == -1 or index2 == -1:
        print("Warning: Attribute for preference not found in mapping.")
        return 'incomparable'

    # Compare the two objects based on the specified preferences
    if object1[index1] == '1' and object2[index2] == '0':
        return 'object1 preferred'
    elif object1[index2] == '0' and object2[index1] == '1':
        return 'object2 preferred'
    
    return 'incomparable'


def parsePreference(preference):
    parts = preference.split('BT')

    if len(parts) != 2:
        raise ValueError(f"Invalid preference format: {preference}")
    
    attributeValuePair1 = parts[0].strip()
    attributeValuePair2 = parts[1].strip()
    attribute1, value1 = attributeValuePair1.split(':')
    attribute2, value2 = attributeValuePair2.split(':')

    return attribute1.strip(), value1.strip(), attribute2.strip(), value2.strip()


if __name__ == "__main__":
    attributes = {
        'dessert': ['cake', 'ice-cream'],
        'drink': ['wine', 'beer'],
    }
    # Generating combinations and encoding them
    combinations = generateCombinations(attributes)
    encodedObjects = encodeCombinations(combinations, attributes)
    
    # Generate mapping and reverse mapping
    mapping, reverseMapping = mapAttributesToIntegers(attributes)
    
    # Proceed with your testing
    print("Encoded Objects:", encodedObjects)

    # New test case output
    print("\nNew Test Case Output:")
    for encodedObject in encodedObjects:
        print(f"Verifying encoded object: {encodedObject}")
        for idx, bit in enumerate(encodedObject):
            attribute = list(attributes.keys())[idx]
            value = attributes[attribute][0 if bit == '1' else 1]
            print(f"Bit: {bit}, Attribute: {attribute}, Value: {value}")

    # Test calculatePenalties
    print("\nTesting calculatePenalties:")
    penaltyLogicRules = [
        ("dessert:cake AND drink:wine", 10),
        ("dessert:ice-cream OR drink:beer", 5),
    ]
    feasibleObjects = ["10", "01"]  # Assuming these are correctly encoded and feasible
    penalties = calculatePenalties(feasibleObjects, penaltyLogicRules, attributes)
    print(f"Penalties: {penalties}")
