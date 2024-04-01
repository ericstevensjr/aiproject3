import itertools, random



def generateCombinations(attributes):
    attributeValues = [values for values in attributes.values()]

    return list(itertools.product(*attributeValues))



def encodeCombinations(combinations, attributes):
    encodedObjects = []

    for combination in combinations:
        encoded = ''.join('0' if val == attributes[attr][1] else '1' for attr, val in zip(attributes.keys(), combination))
        encodedObjects.append(encoded)

    return encodedObjects



def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
        decodedAttributes = []
        
        for bit, (attribute, values) in zip(obj, attributes.items()):
            value = values[0] if bit == '1' else values[1]
            decodedAttributes.append(value)
        print(f"o{idx}: " + ', '.join(decodedAttributes))



def isFeasible(encodedObject, attributes, constraints):
    attributesList = list(attributes.keys())

    for constraint in constraints:
        clauseSatisfied = False

        for literal in constraint:
            isNegated = 'NOT ' in literal
            attributeValue = literal.replace('NOT ', '')

            for attribute, values in attributes.items():
                if attributeValue in values:
                    attributeIndex = attributesList.index(attribute)
                    valueIndex = values.index(attributeValue)
                    bit = '1' if valueIndex == 0 else '0'

                    if isNegated:

                        if encodedObject[attributeIndex] != bit:
                            clauseSatisfied = True
                            break
                    
                    else:
                        if encodedObject[attributeIndex] == bit:
                            clauseSatisfied = True
                            break
        if not clauseSatisfied:
            return False

    return True



def checkFeasibility(encodedObjects, attributes, constraints):
    encodedObjects.reverse()
    feasibilityResults = [(f"o{index}", obj, isFeasible(obj, attributes, constraints)) for index, obj in enumerate(encodedObjects)]
    
    return feasibilityResults



def evaluateCNF(encodedObj, cnfExpression, attributes):
    attributePositions = {attr: i for i, attr in enumerate(attributes)}
    clauses = cnfExpression.split(" AND ")

    for clause in clauses:
        clauseEvaluation = False
        
        literals = clause.split(" OR ")
        for literal in literals:
            negated = "NOT " in literal
            literalAttribute = literal.replace("NOT ", "")
            
            for attr, values in attributes.items():
                if literalAttribute in values:
                    pos = attributePositions[attr]
                    expectedValue = '0' if values.index(literalAttribute) else '1'

                    if negated:
                        expectedValue = '1' if expectedValue == '0' else '0'
                    
                    if encodedObj[pos] == expectedValue:
                        clauseEvaluation = True
                        break

        if not clauseEvaluation:
            return True
    
    return False



def applyPenalties(feasibleObjects, penaltyLogicRules, attributes):
    penaltiesSummary = []

    for objId, encodedObj, _ in feasibleObjects:
        penalties = []

        for cnfExpression, penalty in penaltyLogicRules:

            if evaluateCNF(encodedObj, cnfExpression, attributes):
                penalties.append(penalty)

            else:
                penalties.append(0)

        totalPenalty = sum(penalties)
        penaltiesSummary.append((objId, penalties, totalPenalty))
    
    return penaltiesSummary



def showTable(feasibleObjects, penaltyLogicRules, attributes):
    ruleDescriptions = [rule[0] for rule in penaltyLogicRules]

    # Create the header row dynamically
    headers = ['encoding'] + ruleDescriptions + ['total penalty']
    headerLine = "+" + "+".join(["-" * (len(header) + 2) for header in headers]) + "+"
    headerRow = "| " + " | ".join(headers) + " |"

    print(headerLine)
    print(headerRow)
    print(headerLine)
    feasibleObjects = [(objId, encodedObj, isFeasible) for objId, encodedObj, isFeasible in feasibleObjects if isFeasible]

    penaltiesSummary = applyPenalties(feasibleObjects, penaltyLogicRules, attributes)

    for objId, penalties, totalPenalty in penaltiesSummary:
        penaltiesString = " | ".join(str(p).ljust(14) for p in penalties)
        print(f"| {objId.ljust(10)}| {penaltiesString}| {str(totalPenalty).ljust(13)}|")
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
            return True  
        
    return False  



def evaluatePenaltyCondition(encodedObjects, condition, attributes, map):
    clauses = condition.split(' AND ')

    for clause in clauses:
        isNegated = 'NOT ' in clause
        attrValue = clause.replace('NOT ', '')
        
        for attribute, values in attributes.items():

            if attrValue in values:
                expectedValue = map[attrValue]
                index = list(attributes.keys()).index(attribute)
                actualValue = encodedObjects[index]

                if (isNegated and actualValue == expectedValue) or (not isNegated and actualValue != expectedValue):
                    return 0

    return condition[1]



def exemplification(feasibleObjects, penaltyLogicRules, attributes):
    feasibleObjectsFiltered = [obj for obj in feasibleObjects if obj[2]]  
    objA, objB = random.sample(feasibleObjectsFiltered, 2)
    penaltiesA = applyPenalties([objA], penaltyLogicRules, attributes)[0]  
    penaltiesB = applyPenalties([objB], penaltyLogicRules, attributes)[0]

    if penaltiesA[2] < penaltiesB[2]:  
        print(f"Two randomly selected feasible objects are {penaltiesA[0]} and {penaltiesB[0]},")
        print(f"and {penaltiesA[0]} is strictly preferred over {penaltiesB[0]}.")

    elif penaltiesA[2] > penaltiesB[2]:
        print(f"Two randomly selected feasible objects are {penaltiesA[0]} and {penaltiesB[0]},")
        print(f"and {penaltiesB[0]} is strictly preferred over {penaltiesA[0]}.")

    else:  
        print(f"Two randomly selected feasible objects are {penaltiesA[0]} and {penaltiesB[0]},")
        print("and they are equivalent.")



def omniOptimization(feasibleObjects, penaltyLogicRules, attributes):
    feasibleOnly = [obj for obj in feasibleObjects if obj[2]] 

    penaltiesSummary = applyPenalties(feasibleOnly, penaltyLogicRules, attributes)

    if penaltiesSummary:  
        minTotalPenalty = min(penaltiesSummary, key=lambda x: x[2])[2]

        optimalObjects = [obj for obj in penaltiesSummary if obj[2] == minTotalPenalty]

        print("All optimal objects:", ', '.join(obj[0] for obj in optimalObjects))

    else:
        print("No feasible objects found.")



def ruleAppliesToBothObjects(obj1, obj2, rule, attributes):
    _, condition = rule
    if not condition:  # If there's no condition, the rule applies to both objects by default.
        return True
    
    # Evaluate the condition for both objects.
    conditionMetObject1 = evaluateCondition(obj1[1], condition, attributes)
    conditionMetObject2 = evaluateCondition(obj2[1], condition, attributes)
    
    return conditionMetObject1 and conditionMetObject2



def compareObjectsBasedOnRule(obj1, obj2, rule, attributes):
    preferences, _ = rule

    # Decode objects to access their attributes for comparison
    decodedObject1 = decodeObject(obj1[1], attributes)
    decodedObject2 = decodeObject(obj2[1], attributes)

    # Initialize scores to compare how many preferences each object satisfies
    object1Score = 0
    object2Score = 0

    # Iterate through each preference in the rule
    for preference in preferences:
        # Check if each object satisfies the preference
        if preference in decodedObject1 and decodedObject1[preference] == '1':
            object1Score += 1

        if preference in decodedObject2 and decodedObject2[preference] == '1':
            object2Score += 1



def printExemplificationResult(obj1, obj2, preference):
    obj1ID, obj2ID = obj1[0], obj2[0]

    if preference == "obj1":
        print(f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and {obj1ID} is strictly preferred over {obj2ID}.")

    elif preference == "obj2":
        print(f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and {obj2ID} is strictly preferred over {obj1ID}.")

    elif preference == "equivalent":
        print(f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and they are equivalent.")

    else:
        print(f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and they are incomparable.")


def evaluateCondition(encodedObj, condition, attributes):
    if not condition:  # If there's no condition, it always applies.
        return True
    
    for clause in condition.split(' AND '):
        clauseSatisfied = False

        for literal in clause.split(' OR '):
            attribute, expectedValue = parseLiteral(literal)

            if encodedObj.get(attribute) == expectedValue:
                clauseSatisfied = True
                break  # A single true literal satisfies the clause.

        if not clauseSatisfied:
            return False  # All clauses must be true for the condition to hold.
        
    return True



def decodeObject(encodedObject, attributes):
    decoded = {}

    for bit, attr in zip(encodedObject, attributes.keys()):
        decoded[attr] = '1' if bit == '1' else '0'

    return decoded



def parseLiteral(literal):
    negated = 'NOT ' in literal
    attributeValue = literal.replace('NOT ', '')

    return attributeValue, '0' if negated else '1'



def ruleAppliesToBothObjects(obj1, obj2, rule, attributes):
    _, encodedObj1, _ = obj1
    _, encodedObj2, _ = obj2
    _, condition = rule  
    
    return evaluateCondition(condition, encodedObj1, attributes) and evaluateCondition(condition, encodedObj2, attributes)



def interpretPreferenceRule(preference, attributes):
    preferenceScores = {}
    score = len(preference)  
    for pref in preference:
        for attribute, values in attributes.items():
            if pref in values:
                preferenceScores[attribute] = score
                break
        score -= 1  
    return preferenceScores



def compareObjectsBasedOnPreference(obj1, obj2, preferenceScores):
    obj1Score, obj2Score = 0, 0
    for attribute, score in preferenceScores.items():
        if obj1[attribute] == '1':
            obj1Score += score
        if obj2[attribute] == '1':
            obj2Score += score
    
    if obj1Score > obj2Score:
        return "obj1"
    
    elif obj2Score > obj1Score:
        return "obj2"
    
    else:
        return "incomparable"



def compareObjectsBasedOnRule(obj1, obj2, rule, attributes):
    preferences, _ = rule  
    preferenceScores = interpretPreferenceRule(preferences, attributes)
    obj1Dict = {attr: obj1[1][idx] for idx, attr in enumerate(attributes)}
    obj2Dict = {attr: obj2[1][idx] for idx, attr in enumerate(attributes)}
    
    return compareObjectsBasedOnPreference(obj1Dict, obj2Dict, preferenceScores)



def exemplificationQualitative(feasibleObjects, qualitativeLogicRules, attributes):
    if len(feasibleObjects) < 2:
        print("Not enough feasible objects for comparison.")
        return

    # Select two random feasible objects
    objA, objB = random.sample([obj for obj in feasibleObjects if obj[2]], 2)

    # Decode objects for readability
    decodedObject1 = decodeObject(objA[1], attributes)
    decodedObject2 = decodeObject(objB[1], attributes)

    for rule in qualitativeLogicRules:
        preferences, condition = rule

        # Check if the rule's condition applies to both objects
        if evaluateCondition(objA[1], condition, attributes) and evaluateCondition(objB[1], condition, attributes):
            # If the condition applies, determine the preference based on this rule
            preference = determinePreference(decodedObject1, decodedObject2, [rule], attributes)
            print(f"Comparing {objA[0]} and {objB[0]}: {preference}")

            return  # Exit after evaluating the first applicable rule for simplicity

    print(f"{objA[0]} and {objB[0]} are incomparable.")  # Default outcome if no rules apply or if objects are equal
    
    objA, objB = random.sample([obj for obj in feasibleObjects if obj[2]], 2)
    
    preference = determinePreference(objA, objB, qualitativeLogicRules, attributes)
    
    printExemplificationResult(objA, objB, preference)



def determinePreference(obj1, obj2, rules, attributes):
    for rule in rules:
        # Check if the rule's condition applies to both objects.

        if ruleAppliesToBothObjects(obj1, obj2, rule, attributes):
            preference = compareObjectsBasedOnRule(obj1, obj2, rule, attributes)
            
            # If a preference is determined, return the result immediately.
            if preference != "incomparable":
                obj1ID, obj2ID = obj1[0], obj2[0]

                if preference == "obj1":
                    return f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and {obj1ID} is strictly preferred over {obj2ID}."
                
                else:
                    return f"Two randomly selected feasible objects are {obj1ID} and {obj2ID}, and {obj2ID} is strictly preferred over {obj1ID}."

    # If no preferences could be determined for any of the rules, consider the objects incomparable.
    return "Objects are incomparable based on the rules."



def omniOptimizationQualitative(feasibleObjects, qualitativeLogicRules, attributes):
    optimalObjects = set(obj[0] for obj in feasibleObjects if obj[2])  

    for objA in feasibleObjects:
        for objB in feasibleObjects:
            if objA[0] != objB[0]:
                preference = determinePreference(objA, objB, qualitativeLogicRules, attributes)
                if preference == "objB":
                    optimalObjects.discard(objA[0])  

    print("All optimal objects:", ', '.join(sorted(optimalObjects)))
