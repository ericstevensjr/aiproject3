def parseAttributesFile(filepath):
    attributes = {}
    try:
        with open(filepath, 'r') as attributesFile:
            for line_number, line in enumerate(attributesFile, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    attribute, valuesString = line.split(':')
                    values = [value.strip() for value in valuesString.split(',') if value.strip()]
                    if len(values) != 2 or len(set(values)) != 2:
                        raise ValueError(f"Attribute {attribute} does not have exactly two distinct values.")
                    attributes[attribute.strip()] = values
                except ValueError as e:
                    print(f"Warning: Skipping malformed line {line_number}: {line}. Error: {e}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return attributes

def parseConstraintsFile(filepath):
    constraints = []
    try:
        with open(filepath, 'r') as constraintsFile:
            for line_number, line in enumerate(constraintsFile, 1):
                line = line.strip()
                if line:  # Ensuring the line is not empty
                    # Basic validation of CNF format (could be expanded based on exact format requirements)
                    if not all(literal.strip() for literal in line.split('OR')):
                        print(f"Warning: Malformed CNF clause at line {line_number}: {line}")
                        continue
                    constraints.append(line)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing constraints: {e}")
    return constraints

def parsePenaltyLogicFile(filepath):
    penaltyLogicRules = []
    try:
        with open(filepath, 'r') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    condition, penalty = line.strip().split(',')
                    penalty = int(penalty.strip())  # Ensuring penalty is a non-negative integer
                    if penalty < 0:
                        raise ValueError("Penalty value cannot be negative.")
                    # Basic validation for CNF formula in 'condition' can be added here
                    penaltyLogicRules.append((condition.strip(), penalty))
                except ValueError as ve:
                    print(f"Warning: Skipping malformed penalty logic rule at line {line_number}: {line}. Error: {ve}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing penalty logic rules: {e}")
    return penaltyLogicRules

def parseQualitativeLogicFile(filepath):
    qualitativeLogicRules = []
    try:
        with open(filepath, 'r') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    parts = line.strip().split('IF')
                    if len(parts) != 2:
                        raise ValueError("Rule must contain 'IF' separating condition from preferences.")
                    rule = parts[0].strip()
                    condition = parts[1].strip()
                    # Further validation for the rule's format (e.g., checking for 'BT') can be added here
                    qualitativeLogicRules.append((rule, condition))
                except ValueError as ve:
                    print(f"Warning: Skipping malformed qualitative choice logic rule at line {line_number}: {line}. Error: {ve}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing qualitative choice logic rules: {e}")
    return qualitativeLogicRules
