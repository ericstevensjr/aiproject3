import itertools
from pysat.solvers import Glucose4
import sys

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

def checkFeasibility(objectEncoding, clauses):
    solver = Glucose4()
    # Add hard constraints clauses
    for clause in clauses:
        solver.add_clause(clause)
    
    # Add object-specific clauses
    for i, bit in enumerate(objectEncoding):
        # Assuming mapping starts at 1, adjust accordingly if different
        lit = i + 1
        # If bit is 1, the literal is positive; if 0, it's negated
        clause = [lit] if bit == '1' else [-lit]
        solver.add_clause(clause)
    
    isFeasible = solver.solve()
    solver.delete()  # Clean up the solver instance
    return isFeasible


def inferAttributeFromValue(value, attributes):
    for attribute, values in attributes.items():
        if value in values:
            return attribute
    return None


def evaluateCNF(cnfCondition, encodedObject, mapping, attributes):
    
    # Assuming your CNF evaluation logic is here
    # Debugging output for "fish AND wine"
    if cnfCondition == "fish AND wine":
        print(f"Evaluating 'fish AND wine' for object {encodedObject}")
        # Assuming 'fish' and 'wine' are mapped to bits in the encoding
        fish_bit = mapping["main:fish"] - 1  # Adjust index based on your mapping
        wine_bit = mapping["drink:wine"] - 1
        fish_present = encodedObject[fish_bit] == '1'
        wine_present = encodedObject[wine_bit] == '1'
        print(f"Fish present: {fish_present}, Wine present: {wine_present}")
        return fish_present and wine_present
    for clause in cnfCondition.split(' AND '):
        clauseSatisfied = False
        for literal in clause.split(' OR '):
            negated = 'NOT ' in literal
            value = literal.replace('NOT ', '') if negated else literal

            # Attempt to identify the attribute this value belongs to
            foundAttribute = None
            for attribute, values in attributes.items():
                if value in values:
                    foundAttribute = attribute
                    break
            
            if foundAttribute:
                # Construct the full key using the identified attribute
                fullKey = f"{foundAttribute}:{value}"
                if fullKey in mapping:
                    index = mapping[fullKey] - 1  # Adjust for 0-based indexing
                    expectedValue = '0' if negated else '1'
                    if 0 <= index < len(encodedObject) and encodedObject[index] == expectedValue:
                        clauseSatisfied = True
                        break
                else:
                    print(f"Warning: {fullKey} not properly mapped.")
            else:
                print(f"Warning: Unable to identify attribute for value {value}.")

        if not clauseSatisfied:
            return False
    return True









def calculatePenalties(feasibleObjects, penaltyLogicRules, map, attributes):
    objectPenalties = {}
    for encodedObject in feasibleObjects:
        totalPenalty = 0
        for condition, penalty in penaltyLogicRules:
            if evaluateCNF(condition, encodedObject, map, attributes):
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


def testFeasibility():
    def checkFeasibilityTest(objectEncoding):
        solver = Glucose4()
        # Adding hard constraint for test: NOT wine OR NOT ice-cream
        solver.add_clause([-3, -2])  # Assuming mapping is consistent with the test setup
        
        # Add object-specific clauses based on the encoding
        for i, bit in enumerate(objectEncoding):
            lit = i + 1  # Mapping starts at 1, adjust if different
            clause = [lit] if bit == '1' else [-lit]
            solver.add_clause(clause)
        
        isFeasible = solver.solve()
        solver.delete()  # Clean up the solver instance
        return isFeasible

    # Test 1: Feasible Object (cake, wine, fish) -> Encoding: 101
    test1_encoding = "101"
    test1_result = checkFeasibilityTest(test1_encoding)
    print(f"Test 1 (Feasible) Result: {test1_result}")  # Expected: True

    # Test 2: Infeasible Object (ice-cream, wine, beef) -> Encoding: 011
    test2_encoding = "011"
    test2_result = checkFeasibilityTest(test2_encoding)
    print(f"Test 2 (Infeasible) Result: {test2_result}")  # Expected: False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-feasibility":
        testFeasibility()
    else:
        # Regular program execution logic here
        print("Running the standard program logic.")

        # Example of standard program logic:
        attributes = {
            'dessert': ['cake', 'ice-cream'],
            'drink': ['wine', 'beer'],
            # Add more attributes if needed
        }
        # Here you would proceed with generating combinations, encoding objects, etc.
        # This is where your usual program logic will go when not testing feasibility.