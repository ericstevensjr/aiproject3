import itertools

def parseAttributesFile(filepath):
    attributes = {}
    try:
        with open(filepath, 'r') as attributesFile:
            for line in attributesFile:
                line = line.strip()
                if not line:
                    continue
                try:
                    attribute, valuesString = line.split(':')
                    values = [value.strip() for value in valuesString.split(',') if value.strip()]
                    if attribute.strip() and values:
                        attributes[attribute.strip()] = values
                except ValueError:
                    print(f"Warning: Skipping malformed line: {line}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return attributes


def parseConstraintsFile(filepath):
    constraints = []

    with open(filepath, 'r') as constraintsFile:
        for line in constraintsFile:
            constraint = line.strip()
            constraints.append(constraint)

    return constraints

def parsePenaltyLogicFile(filepath):
    penaltyLogicRules = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                condition, penalty = line.strip().split(',')
                penaltyLogicRules.append((condition.strip(), int(penalty.strip())))
    except FileNotFoundError:
        print(f"File not found: {filepath}. Please make sure the file exists and the path is correct.")
    return penaltyLogicRules

def parseQualitativeLogicFile(filepath):
    qualitiativeLogicRules = []

    with open(filepath, 'r') as file:
        for line in file:
            separateParts = line.strip().split('IF')
            rule = separateParts[0].strip()
            condition = separateParts[1].strip() if len(separateParts) > 1 else ""
            qualitiativeLogicRules.append((rule, condition))
    
    return qualitiativeLogicRules