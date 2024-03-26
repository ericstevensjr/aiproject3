from fileParser import parseAttributesFile, parseConstraintsFile, parsePenaltyLogicFile, parseQualitativeLogicFile
from userInterface import user_interface


def main():
    user_interface(parseAttributesFile, parseConstraintsFile, parsePenaltyLogicFile, parseQualitativeLogicFile)

if __name__ == "__main__":
    main()