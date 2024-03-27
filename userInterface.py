from fileParser import *
from logic import *
import random

def performEncoding(encodedObjects, attributes):
    print("Encoded Objects:")
    attribute_keys = list(attributes.keys())  # Ensure consistent attribute order
    for idx, obj in enumerate(encodedObjects):
        decoded_attributes = []
        for bit_idx, bit in enumerate(obj):
            attribute = attribute_keys[bit_idx]
            # Assuming '0' is for the first listed value and '1' is for the second
            value = attributes[attribute][int(bit)]  # Directly use bit as index
            decoded_attributes.append(value)
        
        object_display = f"o{idx} – " + ', '.join(decoded_attributes)
        print(object_display)


def performFeasibilityChecking(feasibleObjects):
    if feasibleObjects:
        print(f"Yes, there are {len(feasibleObjects)} feasible objects.")
    else:
        print("No feasible objects found.")


def showTable(feasibleObjects, penaltyLogicRules, attributesMapping, attributes):
    # Assuming feasibleObjects is a list of encoded strings representing feasible objects
    # and penaltyLogicRules is a list of tuples (condition, penalty)
    objectPenalties = calculatePenalties(feasibleObjects, penaltyLogicRules, attributesMapping, attributes)
    
    print("+----------+---------------+--------------+---------------+")
    print("| encoding | fish AND wine | wine OR cake | total penalty |")
    print("+----------+---------------+--------------+---------------+")

    for idx, encodedObject in enumerate(feasibleObjects):
        penalties_for_rules = [evaluateCNF(rule[0], encodedObject, attributesMapping, attributes) * rule[1] for rule in penaltyLogicRules]
        total_penalty = sum(penalties_for_rules)
        print(f"| o{idx}      | {' | '.join(str(penalty) for penalty in penalties_for_rules)} | {total_penalty}          |")
        # Adjust the spacing/formatting as needed to match your table's layout

    print("+----------+---------------+--------------+---------------+")




def performExemplification(feasibleObjects, logicRules, preferenceLogic):
    print("Exemplification of two random feasible objects and their preference comparison is under construction.")


def performOmniOptimization(feasibleObjects, logicRules, preferenceLogic):
    print("Finding all optimal feasible objects w.r.t the chosen preference theory is under construction.")


def reasoningTasksMenu(preference_logic, encodedObjects, feasibleObjects, attributes, map, penaltyLogicRules=None, qualitativeLogicRules=None):
    while True:
        print("\nChoose the reasoning task to perform:")
        print("1. Encoding")
        print("2. Feasibility Checking")
        print("3. Show the Table")
        print("4. Exemplification")
        print("5. Omni-optimization")
        print("6. Back to previous menu")
        task_choice = input("Your Choice: ")

        if task_choice == '1':
            performEncoding(encodedObjects, attributes)
        elif task_choice == '2':
            # Example debug print statement
            print(f"Debug: Number of feasible objects: {len(feasibleObjects)}")
            print(f"Debug: Feasible objects list: {feasibleObjects}")
            performFeasibilityChecking(feasibleObjects)
            # When reporting the number of feasible objects
            print(f"Yes, there are {len(feasibleObjects)} feasible objects.")
        elif task_choice == '3':
            logicRules = penaltyLogicRules if preference_logic == 'penalty' else qualitativeLogicRules
            showTable(feasibleObjects, logicRules, map, attributes)
        elif task_choice == '4':
            logicRules = penaltyLogicRules if preference_logic == 'penalty' else qualitativeLogicRules
            performExemplification(feasibleObjects, logicRules, preference_logic)
        elif task_choice == '5':
            logicRules = penaltyLogicRules if preference_logic == 'penalty' else qualitativeLogicRules
            performOmniOptimization(feasibleObjects, logicRules, preference_logic)
        elif task_choice == '6':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def userInterface():
    print("Welcome to PrefAgent!\n")
    
    while True:
        attributesFile = input("Enter Attributes File Name: ")
        constraintsFile = input("Enter Hard Constraints File Name: ")

        attributes = parseAttributesFile(attributesFile)
        print("Parsed Attributes: ", attributes)
        constraints = parseConstraintFile(constraintsFile)
        print("Parsed Constraints: ", constraints)

        combinations = generateCombinations(attributes)
        encodedObjects = encodeCombinations(combinations, attributes)
        print("Encoded Objects: ", encodedObjects)
        print("Length of an Encoded Object: ", len(encodedObjects[0]) if encodedObjects else "N/A")
        map, _ = mapAttributesToIntegers(attributes)
        print("Attribute to Integer Mapping: ", map)
        clauses = convertConstraintsToClauses(constraints, attributes, map)
        print("Constraints as Clauses: ", clauses)
        feasibleObjects = [obj for obj in encodedObjects if checkFeasibility(obj, clauses)]
        print("Feasible Objects:", feasibleObjects)

        preferenceChoice = input("\nChoose the preference logic to use:\n1. Penalty Logic\n2. Qualitative Choice Logic\n3. Exit\nYour Choice: ")
        if preferenceChoice in ['1', '2']:
            preferencesFile = input("Enter Preferences File Name: ")
            if preferenceChoice == '1':
                print("\nYou picked Penalty Logic")
                penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
                reasoningTasksMenu('penalty', encodedObjects, feasibleObjects, attributes, map, penaltyLogicRules=penaltyLogicRules)
            elif preferenceChoice == '2':
                print("\nYou picked Qualitative Choice Logic")
                qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)
                reasoningTasksMenu('qualitative', encodedObjects, feasibleObjects, attributes, map, qualitativeLogicRules=qualitativeLogicRules)
        elif preferenceChoice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")