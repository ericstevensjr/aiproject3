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
    try:
        with open(filepath, 'r') as constraintsFile:
            for line in constraintsFile:
                line = line.strip()
                if line:  # Ensuring the line is not empty
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
            for line in file:
                try:
                    condition, penalty = line.strip().split(',')
                    penalty = int(penalty.strip())  # Ensuring penalty is an integer
                    penaltyLogicRules.append((condition.strip(), penalty))
                except ValueError as ve:
                    print(f"Warning: Skipping malformed penalty logic rule: {line}. Error: {ve}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing penalty logic rules: {e}")
    return penaltyLogicRules


def parseQualitativeLogicFile(filepath):
    qualitativeLogicRules = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                try:
                    parts = line.strip().split('IF')
                    rule = parts[0].strip()
                    condition = parts[1].strip() if len(parts) > 1 else ""
                    qualitativeLogicRules.append((rule, condition))
                except IndexError:
                    print(f"Warning: Skipping malformed qualitative choice logic rule: {line}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"An unexpected error occurred while parsing qualitative choice logic rules: {e}")
    return qualitativeLogicRules
