
import unittest
from src.tests.test_domain.test_entities import TestEntities

domain_test_cases = [TestEntities
                     ]


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()

    for test_class in domain_test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    return suite
