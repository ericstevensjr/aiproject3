import unittest
from fileParser import parseAttributesFile
from logic import evaluatePenaltyLogic, generateEncodedObjects, assignAttributesToVariables, applyConstraints
from unittest.mock import mock_open, patch

class TestFileParser(unittest.TestCase):

    def testParseAttributesFileCorrectFormat(self):
        mockFileContent = "dissert: cake, ice-cream\ndrink: wine, beer\nmain: fish, beef"
        expectedOutput = {
            'dissert': ['cake', 'ice-cream'],
            'drink': ['wine', 'beer'],
            'main': ['fish', 'beef']
        }

        with patch('builtins.open', mock_open(read_data=mockFileContent)):
            self.assertEqual(parseAttributesFile('dummyPath'), expectedOutput)

    def testParseAttributesEmptyFile(self):
        with patch('builtins.open', mock_open(read_data='')):
            self.assertEqual(parseAttributesFile('dummyPath'), {})

        def testParseAttributesFileMalformedLines(self):
            mockFileContent = "dissert: cake, ice-cream\ndrink\nmain: fish, beef"
            expectedOutput = {
                'dissert': ['cake', 'ice-cream'],
                'main': ['fish', 'beef']
            }
            with patch('builtins.open', mock_open(read_data=mockFileContent)):
                self.assertEqual(parseAttributesFile('dummyPath'), expectedOutput)


class TestLogic(unittest.TestCase):

    def testFeasibilityChecking(self):
        attributes = {'dissert': ['cake', 'ice-cream'], 'drink': ['wine', 'beer'], 'main': ['fish', 'beef']}
        constraints = ["NOT wine OR NOT ice-cream"]
        
        encodedObjects = generateEncodedObjects(attributes)
        variableMapping  = assignAttributesToVariables(attributes)
        feasibleObjects = applyConstraints(encodedObjects, constraints, attributes, variableMapping)
        
        # Given the constraint "NOT wine OR NOT ice-cream", the expected feasible objects
        # are all except those with both 'wine' and 'ice-cream'
        # Assuming binary encoding: 'cake' = 1, 'ice-cream' = 0, 'wine' = 1, 'beer' = 0, 'fish' = 1, 'beef' = 0
        # Thus, objects '010' and '011' are NOT feasible.
        expectedFeasibleObjects = ['110', '111', '100', '101', '000', '001']  # Based on your encoding
        
        self.assertCountEqual(feasibleObjects, expectedFeasibleObjects)

    def testPenaltyLogicEvaluation(self):
        # Assuming penaltyLogicRules is correctly parsed from penaltylogic.txt
        penaltyLogicRules = [('fish AND wine', 10), ('wine OR cake', 6)]
        # Example feasible objects (encoded as 'fish,wine', etc., for simplicity)
        feasibleObjects = ['11', '10', '01', '00']  # Simplified binary representation
        attributes = {'fish': ['1', '0'], 'wine': ['1', '0']}
        variableMapping = {'fish:1': 1, 'wine:1': 2}  # Simplified for example
        penalties = evaluatePenaltyLogic(feasibleObjects, penaltyLogicRules, attributes)
        expectedPenalties = {'11': 0, '10': 6, '01': 10, '00': 6}
        self.assertEqual(penalties, expectedPenalties)

if __name__ == '__main__':
    unittest.main()