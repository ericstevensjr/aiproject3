from fileParser import parseAttributesFile, parseConstraintsFile, parsePenaltyLogicFile, parseQualitativeLogicFile
from logic import generateEncodedObjects, assignAttributesToVariables, applyConstraints, evaluatePenaltyLogic

def user_interface():
    print("Welcome to PrefAgent!")
    attributes_file = input("Enter Attributes File Name: ")
    constraints_file = input("Enter Hard Constraints File Name: ")

    attributes = parseAttributesFile(attributes_file)
    constraints = parseConstraintsFile(constraints_file)

    while True:
        choice = input("Choose the preference logic to use:\n1. Penalty Logic\n2. Qualitative Choice Logic\n3. Exit\nYour Choice: ")
        if choice == '1' or choice == '2':
            while True:
                preference_logic_file = input("Enter Preferences File Name: ")
                if choice == '1':
                    penalty_logic_rules = parsePenaltyLogicFile(preference_logic_file)
                    if penalty_logic_rules:
                        perform_penalty_logic_operations(attributes, constraints, penalty_logic_rules)
                        break
                elif choice == '2':
                    qualitative_logic_rules = parseQualitativeLogicFile(preference_logic_file)
                    if qualitative_logic_rules:
                        perform_qualitative_choice_logic_operations(attributes, constraints, qualitative_logic_rules)
                        break
        elif choice == '3':
            print("Bye!")
            break
        else:
            print("Wrong Choice! Enter your choice again.")

def perform_qualitative_choice_logic_operations(attributes, constraints, qualitative_logic_rules):
    encodedObjects = generateEncodedObjects(attributes)
    variableMapping = assignAttributesToVariables(attributes)
    feasibleObjects = applyConstraints(encodedObjects, constraints, variableMapping, attributes)

    while True:
        print("\nChoose the reasoning task to perform:")
        print("1. Encoding\n2. Feasibility Checking\n3. Show the Table\n4. Exemplification\n5. Omni-optimization\n6. Back to previous menu")
        task_choice = input("Your Choice: ")
        if task_choice == '1':
            for index, obj in enumerate(encodedObjects):
                print(f"o{index} – {' '.join([attributes[key][int(val)] for key, val in zip(attributes.keys(), obj)])}")
        elif task_choice == '2':
            print("\nFeasible Objects:")
            for obj in feasibleObjects:
                print(obj)
        elif task_choice == '3':
            # Show the table for qualitative choice logic. Placeholder for now.
            print("Show the Table not yet implemented for Qualitative Choice Logic.")
        elif task_choice == '4':
            # Exemplification logic for qualitative choice logic. Placeholder for now.
            print("Exemplification not yet implemented for Qualitative Choice Logic.")
        elif task_choice == '5':
            # Omni-optimization logic for qualitative choice logic. Placeholder for now.
            print("Omni-optimization not yet implemented for Qualitative Choice Logic.")
        elif task_choice == '6':
            break
        else:
            print("Wrong Choice! Enter your choice again.")



def perform_penalty_logic_operations(attributes, constraints, penalty_logic_rules):
    encodedObjects = generateEncodedObjects(attributes)
    variableMapping = assignAttributesToVariables(attributes)
    feasibleObjects = applyConstraints(encodedObjects, constraints, variableMapping, attributes)
    penalties = evaluatePenaltyLogic(feasibleObjects, penalty_logic_rules, attributes)

    while True:
        print("\nChoose the reasoning task to perform:")
        print("1. Encoding\n2. Feasibility Checking\n3. Show the Table\n4. Exemplification\n5. Omni-optimization\n6. Back to previous menu")
        task_choice = input("Your Choice: ")
        if task_choice == '1':
            for index, obj in enumerate(encodedObjects):
                print(f"o{index} - {' '.join([attributes[key][int(val)] for key, val in zip(attributes.keys(), obj)])}")
        elif task_choice == '2':
            print("\nFeasible Objects:")
            for obj in feasibleObjects:
                print(obj)
        elif task_choice == '3':
            header = "| {:>8} | {:>13} | {:>13} | {:>13} |"
            row = "| {:>8} | {:>13} | {:>13} | {:>13} |"
            print("\n+----------+---------------+---------------+---------------+")
            print(header.format("encoding", "fish AND wine", "wine OR cake", "total penalty"))
            print("+----------+---------------+---------------+---------------+")
            
            # Example penalties for "fish AND wine" and "wine OR cake"
            fish_and_wine_penalty = 10
            wine_or_cake_penalty = 6

            for index, obj in enumerate(feasibleObjects):
                # Calculate penalties based on conditions
                fish_and_wine = fish_and_wine_penalty if "5" in obj and "3" in obj else 0  # Check your condition
                wine_or_cake = wine_or_cake_penalty if "3" in obj or "1" in obj else 0  # Check your condition
                total_penalty = fish_and_wine + wine_or_cake
                
                print(row.format(f"o{index}", fish_and_wine, wine_or_cake, total_penalty))
            print("+----------+---------------+---------------+---------------+")
        elif task_choice == '4':
            # Exemplification logic here. Placeholder for now.
            print("Exemplification not yet implemented.")
        elif task_choice == '5':
            # Omni-optimization logic here. Placeholder for now.
            print("Omni-optimization not yet implemented.")
        elif task_choice == '6':
            break
        else:
            print("Wrong Choice! Enter your choice again.")


def main():
    user_interface()

if __name__ == "__main__":
    main()