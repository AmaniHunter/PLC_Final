import re
from Token import Token

class Lexer:
    def __init__(self, amaniCode):
        self.amaniCode = amaniCode
        self.tokens = []
        self.tokenDictionary = {0: 'real_literal', 1: 'natural_literal', 2: 'bool_literal', 3: 'char_literal',
                                4: 'string_literal', 5: 'string_literal', 6: 'if statement', 7: 'else statement',
                                8: 'elif statement', 9: 'while loop', 10: 'String declaration',
                                11: 'int declaration',
                                12: 'char declaration', 13: 'float declaration', 14: 'boolean declaration',
                                15: 'function declaration',
                                16: 'addition symbol', 17: 'subtraction symbol', 18: 'multiplication symbol',
                                19: 'division symbol',
                                20: 'modulus symbol', 21: 'exponentiation symbol', 22: 'left parentheses',
                                23: 'right parentheses',
                                24: 'greater than or equal too symbol', 25: 'less than or equal too symbol',
                                26: 'greater than symbol',
                                27: 'less than symbol', 28: 'equal too symbol', 29: 'not equal too symbol',
                                30: 'assignment symbol',
                                31: 'unary negation symbol', 32: 'logical not symbol', 33: 'logical and symbol',
                                34: 'logical or symbol',
                                35: 'left curly brace', 36: 'right curly brace', 37: 'parameter separator',
                                38: 'variable or function identifier'}

    def ignoreComments(self):
        commentRegex = "('''[\\s\\S]*''')|(#.*)"
        self.amaniCode = re.sub(commentRegex, '', self.amaniCode)

    def tokenizer(self):
        self.ignoreComments()
        self.amaniCode = self.amaniCode.strip()

        # this regex allows + or - and decimals
        realLiteralRegex = "([-+]?[0-9]*[.][0-9]+)"

        # this regex allows an int to have + or - in front of it
        naturalLiteralRegex = "([-+]?[0-9]+)"

        # this regex allows true or false and is case sensitive. no alpha numeric chars
        boolLiteralRegex = "((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|" + \
                             "(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))"

        # this regex allows one character to ascii code and in place between ' '
        charLiteralRegex = "('\\\\?[ -~]')"

        # this regex allows non chars
        stringLiteralRegex = "('(\\\\.|[^\'\\\\])*')"

        # building keyword regex...
        keywordRegex = ['if','else','elif','while', 'String','int','char','float','bool', 'def']

        # examine keyword by looking ahead and behind
        for i in range(len(keywordRegex)):
            keywordRegex[i] = "((?<![a-zA-Z0-9_])" + keywordRegex[i] + "(?![a-zA-Z0-9_]))"
        keywordRegex = "|".join(keywordRegex)

        # this regex allows for special symbols such as bool ops, code separation, math ops
        specialSymbolsRegex = "(\+)|(\-)|(\*)|(\/)|(\%)|(\^)|(\()|(\))|" + \
                                "(\>\=\=)|(\<\=\=)|(\>)|(\<)|(\=\=)|(\!\=\=)|(\=)|(\~)|(\!)|(\&)|" + \
                                "(\|)|(\{)|(\})|(\,)"

        # variable and function name without a leading number.
        varOrFuncIdentifierRegex = "([a-zA-Z_][a-zA-Z0-9_]*)"

        # combining all
        regex = realLiteralRegex
        regex += "|" + naturalLiteralRegex
        regex += "|" + boolLiteralRegex
        regex += "|" + charLiteralRegex
        regex += "|" + stringLiteralRegex
        regex += "|" + keywordRegex
        regex += "|" + specialSymbolsRegex
        regex += "|" + varOrFuncIdentifierRegex

        lexemeIndex = 0

        # gets first match
        match = re.match(regex, self.amaniCode)

        # read each token until at the end of file
        while match is not None and match[0]:
           # print('here')
            self.amaniCode = self.amaniCode.replace(match[0], '', 1)
            self.amaniCode = self.amaniCode.lstrip()

            self.tokens.append(Token(match[0],match.groups().index(match[0])))

            print('Lexeme at index {:2d} is: {:16s} Token is ({:2d}) {:s}'.format(lexemeIndex, match[0], match.groups().index(match[0]),
                                                                                  self.tokenDictionary[match.groups().index(match[0])]))
            lexemeIndex += 1
            match = re.match(regex, self.amaniCode)

        # if returning true all tokens are valid. else return false thus ending processinng
        if len(self.amaniCode) > 0:
            return False
        return True
