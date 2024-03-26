def parseAttributesFile(filepath):
    attributes = {}

    try:
        with open(filepath, 'r') as file:
            for lineNumber, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) != 2:
                    print(f"Warning: Line {lineNumber} is malfromed, skipping: {line}")
                    continue
                attribute, valuesString = parts
                values = [value.strip() for value in valuesString.split(',') if value.strip()]
                if len(values) != 2:
                    print(f"Warning: Attribute '{attribute}' does not have exactly two values, skipping: {line}")
                    continue
                attributes[attribute.strip()] = values
    
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return {}
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
    
    return attributes


def parseConstraintFile(filepath):
    constraints = []

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                literals = [literal.strip() for literal in line.split('OR')]
                constraints.append(literals)

    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []
    
    except Exception as e:
        print(f"An unexpected error occurred while parsing constraints: {e}")
        return []
    
    return constraints


def parsePenaltyLogicFile(filepath):
    penaltyLogicRules = []

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    condition, penalty = line.split(',')
                    penalty = int(penalty.strip())
                    penaltyLogicRules.append((condition.strip(), penalty))
                
                except ValueError:
                    print(f"Warning: Skipping malformed penalty logic rule: {line}")

    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []
    
    except Exception as e:
        print(f"An unexpected error occurred while parsing penalty logic rules: {e}")
        return []
    
    return penaltyLogicRules
            

def parseQualitativeLogicFile(filepath):
    qualitativeLogicRules = []

    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('IF')
                condition = parts[1].strip() if len(parts) > 1 else ""
                preferences = parts[0].strip()
                qualitativeLogicRules.append((preferences, condition))
    
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []
    
    except Exception as e:
        print(f"An unexpected error occurred while parsing qualitative choice logic rules: {e}")
        return []
    
    return qualitativeLogicRules


