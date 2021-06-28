import random


def create_slug_code(n: int = 5):
    """Generate code"""
    code_characters = 'abcdefghijklnopqrstuvwxyz1234567890'
    return ''.join([code_characters[random.randrange(0, len(code_characters))] for i in range(n)])