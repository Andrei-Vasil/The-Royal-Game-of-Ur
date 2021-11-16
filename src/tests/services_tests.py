
import unittest

from src.tests.test_services.test_ai_strategy import TestAIStrategy
from src.tests.test_services.test_game_controller import TestGameController
from src.tests.test_services.test_board import TestBoard

services_test_cases = [TestGameController,
                       TestBoard,
                       TestAIStrategy
                       ]


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()

    for test_class in services_test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    return suite
