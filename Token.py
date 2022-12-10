import string


class Token:
    
    def __init__(self, lexeme, code):
        self.lexeme = lexeme
        self.code = code