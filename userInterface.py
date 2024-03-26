from fileParser import *
from logic import *
import random

def performEncoding(encodedObjects):
    print("Encoded Objects:")
    for obj in encodedObjects:
        print(obj)


def performFeasibilityChecking(feasibleObjects):
    if feasibleObjects:
        print(f"Yes, there are {len(feasibleObjects)} feasible objects.")
    else:
        print("No feasible objects found.")


def showTable(feasibleObjects, logicRules, preferenceLogic, map):
    if preferenceLogic == 'penalty':
        # Prepare the header
        headers = ["Encoding"] + [f"Rule {i+1}" for i in range(len(logicRules))] + ["Total Penalty"]
        header_row = "{:<10} " + " ".join(["{:<10}" for _ in range(len(logicRules))]) + " {:<14}"
        print(header_row.format(*headers))

        # Print separator
        print("-" * (12 + 11 * len(logicRules) + 15))

        # Iterate over each feasible object and display the calculated penalties
        for obj in feasibleObjects:
            row_data = [obj]
            totalPenalty = 0
            for condition, penalty in logicRules:
                if evaluateCNF(condition, obj, map):
                    row_data.append(str(penalty))
                    totalPenalty += penalty
                else:
                    row_data.append('0')
            row_data.append(str(totalPenalty))
            
            # Format and print each row
            row_format = "{:<10} " + " ".join(["{:<10}" for _ in range(len(logicRules))]) + " {:<14}"
            print(row_format.format(*row_data))


def performExemplification(feasibleObjects, logicRules, preferenceLogic):
    print("Exemplification of two random feasible objects and their preference comparison is under construction.")


def performOmniOptimization(feasibleObjects, logicRules, preferenceLogic):
    print("Finding all optimal feasible objects w.r.t the chosen preference theory is under construction.")


def reasoningTasksMenu(preference_logic, feasibleObjects, attributes, map, penaltyLogicRules=None, qualitativeLogicRules=None):
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
            performEncoding(feasibleObjects)
        elif task_choice == '2':
            performFeasibilityChecking(feasibleObjects)
        elif task_choice == '3':
            logicRules = penaltyLogicRules if preference_logic == 'penalty' else qualitativeLogicRules
            showTable(feasibleObjects, logicRules, preference_logic, map)
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
        map, _ = mapAttributesToIntegers(attributes)
        print("Attribute to Integer Mapping: ", map)
        clauses = convertConstraintsToClauses(constraints, attributes, map)
        print("Constraints as Clauses: ", clauses)
        feasibleObjects = [obj for obj in encodedObjects if checkFeasibility(clauses)]

        preferenceChoice = input("\nChoose the preference logic to use:\n1. Penalty Logic\n2. Qualitative Choice Logic\n3. Exit\nYour Choice: ")
        if preferenceChoice in ['1', '2']:
            preferencesFile = input("Enter Preferences File Name: ")
            if preferenceChoice == '1':
                print("\nYou picked Penalty Logic")
                penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
                reasoningTasksMenu('penalty', feasibleObjects, attributes, map, penaltyLogicRules=penaltyLogicRules)
            elif preferenceChoice == '2':
                print("\nYou picked Qualitative Choice Logic")
                qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)
                reasoningTasksMenu('qualitative', feasibleObjects, attributes, map, qualitativeLogicRules=qualitativeLogicRules)
        elif preferenceChoice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")