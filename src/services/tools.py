import string
import random


class Color:
    """
        Colors for console printing. Very important!
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class RandomGenerator:
    """
        It says in the name, it's a random generator! Generates random stuff!
    """
    @staticmethod
    def generate_string(length=10) -> str:
        """
        Generates a random string.
        :param length: the desired length of the random string. Default is 10. (int)
        :return: a random string of how many characters you want
        """
        allowed_chars = string.ascii_uppercase + string.digits

        generated_string = ""

        for i in range(length):
            token = allowed_chars[random.randint(0, len(allowed_chars) - 1)]
            generated_string += token

        return generated_string

    @staticmethod
    def generate_number(min_value=1, max_value=10) -> int:
        """
        Generates an integer between min_value and max_value
        :param min_value: the minimum value you might want as your integer
        :param max_value: the maximum value you might want as your integer
        :return: a random integer
        """
        return random.randint(min_value, max_value)
