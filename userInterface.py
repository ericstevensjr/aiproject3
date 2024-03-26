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


def showTable(feasibleObjects, penaltyLogicRules, preferenceLogic, map, attributes):
    print(feasibleObjects[:5])
    if preferenceLogic == 'penalty':
        # Headers
        headers = ["encoding"] + [condition for condition, _ in penaltyLogicRules] + ["total penalty"]

        # Calculate penalties for each object and sort by total penalty
        penalties_data = []
        for idx, obj in enumerate(feasibleObjects, 1):
            penalties = [evaluateCNF(condition, obj, map, attributes) * penalty for condition, penalty in penaltyLogicRules]
            total_penalty = sum(penalties)
            penalties_data.append((f"o{idx}", *penalties, total_penalty))

        # Sort by total penalty, highest first
        penalties_data.sort(key=lambda x: x[-1], reverse=True)

        # Determine column widths
        column_widths = [max(len(str(row[i])) for row in [headers] + penalties_data) + 2 for i in range(len(headers))]

        # Print header
        header_row = "|" + "|".join(header.center(width) for header, width in zip(headers, column_widths)) + "|"
        print("-" * len(header_row))
        print(header_row)
        print("-" * len(header_row))

        # Print rows
        for row in penalties_data:
            print("|" + "|".join(str(val).rjust(width) for val, width in zip(row, column_widths)) + "|")
        print("-" * len(header_row))


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
            showTable(feasibleObjects, logicRules, preference_logic, map, attributes)
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
        print("Encoded Objects (sample):", encodedObjects[:5])
        print("Length of an Encoded Object:", len(encodedObjects[0]) if encodedObjects else "N/A")
        map, _ = mapAttributesToIntegers(attributes)
        print("Attribute to Integer Mapping: ", map)
        clauses = convertConstraintsToClauses(constraints, attributes, map)
        print("Constraints as Clauses: ", clauses)
        feasibleObjects = [obj for obj in encodedObjects if checkFeasibility(clauses)]
        print("Feasible Objects:", feasibleObjects[:5])

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