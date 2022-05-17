import unittest
from tests.test_parsers import TestExtractor
from tests.test_manager import TestManager
from tests.test_tags import TestBaseTag

test_cases = [
    TestExtractor,
    TestManager,
    TestBaseTag
]


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    unittest.main()
