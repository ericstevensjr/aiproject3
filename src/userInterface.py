from fileParser import *
from logic import *

def reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, preferenceChoice , penaltyLogicRules=None, qualitativeLogicRules=None):
    while True:
        print("\nChoose the reasoning task to perform:")
        print("1. Encoding")
        print("2. Feasibility Checking")
        print("3. Show the Table")
        print("4. Exemplification")
        print("5. Omni-optimization")
        print("6. Back to previous menu")
        taskChoice = input("\nYour Choice: ")

        if taskChoice == '1':
            performEncoding(encodedObjects, attributes)

        elif taskChoice == '2':

            if feasibleObjects:
                feasibleObjectsCount = sum(1 for _, _, isObjFeasible in feasibleObjects if isObjFeasible)
                print(f"Yes, there are {feasibleObjectsCount} feasible objects.")

            else:
                print("No feasible objects found.")

        elif taskChoice == '3':

            if penaltyLogicRules:
                showTable(feasibleObjects, penaltyLogicRules, attributes)

            else:
                print("No penalty logic rules provided.")

        elif taskChoice == '4':

            if preferenceChoice == '1':
                exemplification(feasibleObjects, penaltyLogicRules, attributes)

            elif preferenceChoice == '2':
                exemplificationQualitative(feasibleObjects, qualitativeLogicRules, attributes)

        elif taskChoice == '5':
                
                if preferenceChoice == '1':
                    omniOptimization(feasibleObjects, penaltyLogicRules, attributes)

                else:
                    omniOptimizationQualitative(feasibleObjects, qualitativeLogicRules, attributes)

        elif taskChoice == '6':
            print("\nChoose the preference logic to use:")
            print("1. Penalty Logic")
            print("2. Qualitative Choice Logic")
            print("3. Exit")
            preferenceChoice = input("\nYour Choice: ")

            if preferenceChoice == '1':
                print("\nYou picked Penalty Logic")
                preferencesFile = input("Enter Preferences File Name: ")
                penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
                reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, preferenceChoice, penaltyLogicRules=penaltyLogicRules)

            elif preferenceChoice == '2':
                print("\nYou picked Qualitative Choice Logic")
                preferencesFile = input("Enter Preferences File Name: ")
                qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)
                reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, preferenceChoice, qualitativeLogicRules=qualitativeLogicRules)
            
            elif preferenceChoice == '3':
                print("Exiting. Goodbye!")
                break
            
            else:
                print("\nWrong choice! Please your choice: ")
                continue



def userInterface():
    print("Welcome to PrefAgent!\n")

    attributesFile = input("Enter Attributes File Name: ")
    constraintsFile = input("\nEnter Hard Constraints File Name: ")
    attributes = parseAttributesFile(attributesFile)
    constraints = parseConstraintFile(constraintsFile)
    encodedObjects = encodeCombinations(generateCombinations(attributes), attributes)
    feasibleObjects = checkFeasibility(encodedObjects, attributes, constraints)

    while True:
        print("\nChoose the preference logic to use:")
        print("1. Penalty Logic")
        print("2. Qualitative Choice Logic")
        print("3. Exit")
        preferenceChoice = input("\nYour Choice: ")

        if preferenceChoice == '1':
            print("\nYou picked Penalty Logic")
            preferencesFile = input("Enter Preferences File Name: ")
            penaltyLogicRules = parsePenaltyLogicFile(preferencesFile)
            reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, preferenceChoice, penaltyLogicRules=penaltyLogicRules)

        elif preferenceChoice == '2':
            print("\nYou picked Qualitative Choice Logic")
            preferencesFile = input("Enter Preferences File Name: ")
            qualitativeLogicRules = parseQualitativeLogicFile(preferencesFile)

            reasoningTasksMenu(attributes, encodedObjects, feasibleObjects, constraints, preferenceChoice, qualitativeLogicRules=qualitativeLogicRules)
        elif preferenceChoice == '3':
            print("\Bye!")
            break
        
        else:
            continue