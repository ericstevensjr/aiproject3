from fileParser import *
from logic import *

def reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, penaltyLogicRules=None, qualitativeLogicRules=None):
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
            # Assuming constraints are already parsed and available in a suitable format
            # And assuming attributes and encodedObjects are defined and available
            # Inform the user about the result of the feasibility check
            if feasibleObjects:
                print(f"There are {len(feasibleObjects)} feasible objects.")
                # Optionally, list the feasible objects or perform further actions with them
            else:
                print("No feasible objects found.")
        elif task_choice == '3':
            if penaltyLogicRules:
                showTable(feasibleObjects, penaltyLogicRules, attributes)
            else:
                print("No penalty logic rules provided.")
        elif task_choice == '4':
            print("Exemplification not implemented.")  # Placeholder for actual functionality
        elif task_choice == '5':
            print("Omni-optimization not implemented.")  # Placeholder for actual functionality
        elif task_choice == '6':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def userInterface():
    print("Welcome to PrefAgent!\n")

    attributesFile = input("Enter Attributes File Name: ")
    constraintsFile = input("Enter Hard Constraints File Name: ")
    attributes = parseAttributesFile(attributesFile)
    constraints = parseConstraintFile(constraintsFile)
    encodedObjects = encodeCombinations(generateCombinations(attributes), attributes)
    # Assuming there's logic here to apply constraints and find feasibleObjects
    feasibleObjects = checkFeasibility(encodedObjects, constraints, attributes)

    while True:
        print("Choose the preference logic to use:")
        print("1. Penalty Logic")
        print("2. Qualitative Choice Logic")
        print("3. Exit")
        preferenceChoice = input("Your Choice: ")

        if preferenceChoice == '1':
            preferencesFile = input("Enter Preferences File Name: ")
            penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
            print("\nYou picked Penalty Logic")
            reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, penaltyLogicRules=penaltyLogicRules)
        elif preferenceChoice == '2':
            preferencesFile = input("Enter Preferences File Name: ")
            qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)
            print("\nYou picked Qualitative Choice Logic")
            reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, qualitativeLogicRules=qualitativeLogicRules)
        elif preferenceChoice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    userInterface()
