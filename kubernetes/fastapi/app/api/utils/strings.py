import random
import string

class StringUtils:
    @staticmethod
    def slugify(text):
        return text.lower().replace(" ", "-")

    @staticmethod
    def random_string(length: int, chars:bool=True, digits:bool=False, special_characters:bool=False):
        chars = ""
        if chars:
            chars += string.ascii_letters
        if digits:
            chars += string.digits
        if special_characters:
            chars += "[~!@#$%^&*]"
        
        return ''.join(random.choice(chars) for _ in range(length))