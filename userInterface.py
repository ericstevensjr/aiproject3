from fileParser import *
from logic import *
import random

def userInterface():
    print("Welcome to PrefAgent!\n")
    
    attributesFile = input("Enter Attributes File Name: \n")
    constraintsFile = input("Enter Hard Constraints File Name: ")

    attributes = parseAttributesFile(attributesFile)
    constraints = parseConstraintFile(constraintsFile)

    combinations = generateCombinations(attributes)
    encodedObjects = encodeCombinations(combinations, attributes)
    map = mapAttributesToIntegers(attributes)
    clauses = convertConstraintsToClauses(constraints, map)
    feasibleObjects = [object for object in encodedObjects if checkFeasibility(clauses)]

    choice = input("Choose the preference logic to use:\n1. Penalty Logic\n2. Qualitative Choice Logic\n3. Exit\nYour Choice: ")

    if choice == '1':
        print("\nYou picked Penalty Logic\n")
        
        perferencesFile = input("Enter Preferences File Name: ")
        penaltyLogicRules = parsePenaltyLogicFile(perferencesFile)
        objectPenalties = calculatePenalties(feasibleObjects, penaltyLogicRules, map)

        print("\nFeasible Objects and their Penalties:")
        for object, penalty in objectPenalties.items():
            print(f"{object}: {penalty}")
    
    elif choice == '2':
        print("\nYou picked Qualitative Choice Logic\n")
        
        qclPreferencesFile = input("Enter Preferences File Name: ")
        qualitativeLogicRules = parseQualitativeLogicFile(qclPreferencesFile)
        
        print("Qualitative Choice Logic functionality is under construction.")

        return
    
    elif choice == '3':
        print("Exiting. Goodbye!")

        return
    
    else:
        print("Invalid choice. Please restart and select a valid opiton.")
        
        return
        
        

if __name__ == "__main__":
    userInterface()