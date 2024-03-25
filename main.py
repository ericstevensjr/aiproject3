from fileParser import parseAttributesFile, parseConstraintsFile, parsePenaltyLogicFile, parseQualitativeLogicFile
from logic import generateEncodedObjects, assignAttributesToVariables, applyConstraints, evaluatePenaltyLogic

def main():
    attributes = parseAttributesFile('attributes.txt')
    constraints = parseConstraintsFile('constraints.txt')
    penaltyLogicRules = parsePenaltyLogicFile('penaltylogic.txt')
    qualitativeLogicRules = parseQualitativeLogicFile('qualitativechoicelogic.txt')

    encodedObjects = generateEncodedObjects(attributes)
    variableMapping = assignAttributesToVariables(attributes)
    feasibleObjects = applyConstraints(encodedObjects, constraints, attributes)
    penalties = evaluatePenaltyLogic(feasibleObjects, penaltyLogicRules, variableMapping, attributes)

    print("Feasible Objects:", feasibleObjects)
    print("Penalties", penalties)

if __name__ == "__main__":
    main()