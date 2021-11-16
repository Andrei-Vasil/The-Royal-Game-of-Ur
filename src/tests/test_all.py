
import unittest
from src.tests import domain_tests, repo_tests, services_tests


test_modules = [domain_tests, repo_tests, services_tests]

loader = unittest.TestLoader()
suite = unittest.TestSuite()

for test_module in test_modules:
    # noinspection PyTypeChecker
    suite.addTests(loader.loadTestsFromModule(test_module))


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
