
import unittest
from src.tests.test_repo.test_repo import TestRepo

repo_test_cases = [TestRepo
                   ]


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()

    for test_class in repo_test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    return suite
