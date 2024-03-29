def parseAttributesFile(filename):
    """
    Parses the attributes file.
    The file format is expected to have one attribute per line,
    with the attribute name followed by its two possible values, separated by commas.
    """
    attributes = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                attr_name, values = parts
                attributes[attr_name.strip()] = [value.strip() for value in values.split(',')]
    return attributes

def parseConstraintFile(filename):
    """
    Parses the constraints file.
    The file format expects each constraint as a CNF clause on a separate line.
    """
    constraints = []
    with open(filename, 'r') as file:
        for line in file:
            # Assuming each line is a single constraint consisting of literals separated by ' OR '
            # and optionally prefixed with 'NOT ' for negation.
            constraint = [literal.strip() for literal in line.strip().split('OR')]
            constraints.append(constraint)
    return constraints

def parsePenaltyLogicFile(filename):
    """
    Parses the penalty logic file.
    Each row describes one penalty logic rule which is a comma-separated pair:
    a CNF propositional formula and a penalty value.
    """
    penaltyLogicRules = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                cnfFormula, penalty = parts[0].strip(), int(parts[1].strip())
                penaltyLogicRules.append((cnfFormula, penalty))
    return penaltyLogicRules

def parseQualitativeLogicFile(filename):
    """
    Parses the qualitative choice logic file.
    Each row describes one qualitative choice logic rule in the format "φ1 BT ... φn IF ψ".
    """
    qualitativeLogicRules = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('IF')
            if len(parts) == 2:
                preferences, condition = parts[0].strip(), parts[1].strip()
                # Splitting preferences on 'BT' to handle multiple preferences if needed
                preferences = [pref.strip() for pref in preferences.split('BT')]
                qualitativeLogicRules.append((preferences, condition))
            elif len(parts) == 1:
                # Handle cases with no conditions
                preferences = [pref.strip() for pref in parts[0].split('BT')]
                qualitativeLogicRules.append((preferences, ''))
    return qualitativeLogicRules
