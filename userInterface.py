from fileParser import parseAttributesFile, parseConstraintFile, parsePenaltyLogicFile, parseQualitativeLogicFile
from logic import generateCombinations, encodeCombinations, convertConditionToManualClauses, checkFeasibility, evaluateCNFManually

def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    for idx, obj in enumerate(encodedObjects):
        decoded_attributes = [attributes[attr][int(bit)] for attr, bit in zip(attributes.keys(), obj)]
        print(f"o{idx} – " + ', '.join(decoded_attributes))

def performFeasibilityChecking(feasibleObjects):
    if feasibleObjects:
        print(f"Yes, there are {len(feasibleObjects)} feasible objects.")
    else:
        print("No feasible objects found.")

def showTable(feasibleObjects, penaltyLogicRules, attributes):
    print("+----------+---------------+--------------+---------------+")
    print("| encoding | fish AND wine | wine OR cake | total penalty |")
    print("+----------+---------------+--------------+---------------+")
    
    for idx, obj in enumerate(feasibleObjects):
        total_penalty = 0
        for condition, penalty in penaltyLogicRules:
            manualClauses = convertConditionToManualClauses(condition, attributes)
            if evaluateCNFManually(obj, manualClauses, attributes):
                total_penalty += penalty
        print(f"| o{idx:<8}| {'Dynamic penalty display not implemented'} | {total_penalty:<13}|")
    print("+----------+---------------+--------------+---------------+")

def userInterface():
    print("Welcome to PrefAgent!\n")

    attributesFile = input("Enter Attributes File Name: ")
    constraintsFile = input("Enter Hard Constraints File Name: ")
    attributes = parseAttributesFile(attributesFile)
    constraints = parseConstraintFile(constraintsFile)

    combinations = generateCombinations(attributes)
    encodedObjects = encodeCombinations(combinations, attributes)
    # Process constraints here as needed for your logic, not shown for brevity
    feasibleObjects = checkFeasibility(encodedObjects, [[[]]], attributes)  # Placeholder for actual constraint processing

    while True:
        preferenceChoice = input("\nChoose the preference logic to use:\n1. Penalty Logic\n2. Qualitative Choice Logic\n3. Exit\nYour Choice: ")
        if preferenceChoice in ['1', '2']:
            preferencesFile = input("Enter Preferences File Name: ")
            if preferenceChoice == '1':
                print("\nYou picked Penalty Logic")
                penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
                showTable(feasibleObjects, penaltyLogicRules, attributes)
                # Additional logic for other choices as needed
            elif preferenceChoice == '2':
                print("Qualitative Choice Logic processing not implemented.")
        elif preferenceChoice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    userInterface()
