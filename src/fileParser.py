def parseAttributesFile(filename):
    attributes = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                attributeName, values = parts
                attributes[attributeName.strip()] = [value.strip() for value in values.split(', ')]

    return attributes

def parseConstraintFile(filename):
    constraints = []

    with open(filename, 'r') as file:
        for line in file:
            # Assuming each line is a single constraint consisting of literals separated by ' OR '
            # and optionally prefixed with 'NOT ' for negation.
            constraint = [literal.strip() for literal in line.strip().split(' OR ')]
            constraints.append(constraint)
    
    return constraints

def parsePenaltyLogicFile(filename):
    penaltyLogicRules = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                cnfFormula, penalty = parts[0].strip(), int(parts[1].strip())
                penaltyLogicRules.append((cnfFormula, penalty))

    return penaltyLogicRules

def parseQualitativeLogicFile(filename):
    qualitativeLogicRules = []

    with open(filename, 'r') as file:
        for line in file:
            # Splitting the line on " IF " to separate the conditional part, if present.
            parts = line.strip().split(' IF ')
            preference_part = parts[0].strip()
            condition = parts[1].strip() if len(parts) > 1 else ''

            # Now, split the preference part on ' BT ' to get the list of preferences.
            preferences = preference_part.split(' BT ')

            # Checking if the last preference accidentally includes " IF"
            if preferences and " IF" in preferences[-1]:
                # Split the last preference to remove any trailing " IF"
                lastPreference, _, potentialCondition = preferences[-1].rpartition(" IF")
                preferences[-1] = lastPreference.strip()  # Update the last preference without " IF"
                if potentialCondition:  # If there's a condition extracted here, it should take precedence
                    condition = potentialCondition
            qualitativeLogicRules.append((preferences, condition))

    return qualitativeLogicRules




