import unittest
from fileParser import parseAttributesFile
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

if __name__ == '__main__':
    unittest.main()