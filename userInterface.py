from fileParser import *
from logic import *
def reasoningTasksMenu(attributes, feasibleObjects, penaltyLogicRules=None, qualitativeLogicRules=None):
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
            encodedObjects = encodeCombinations(generateCombinations(attributes), attributes)
            performEncoding(encodedObjects, attributes)
        elif task_choice == '2':
            print("Feasibility Checking not fully implemented.")  # Placeholder for actual functionality
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

    # Assuming there's logic here to apply constraints and find feasibleObjects
    feasibleObjects = []  # Placeholder for feasible objects based on constraints

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
            reasoningTasksMenu(attributes, feasibleObjects, penaltyLogicRules=penaltyLogicRules)
        elif preferenceChoice == '2':
            preferencesFile = input("Enter Preferences File Name: ")
            qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)
            print("\nYou picked Qualitative Choice Logic")
            reasoningTasksMenu(attributes, feasibleObjects, qualitativeLogicRules=qualitativeLogicRules)
        elif preferenceChoice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    userInterface()
