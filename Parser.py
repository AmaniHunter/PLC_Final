import re
from ParseTree import ParseTree

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.parseTree = ParseTree()
        self.currentParse = self.parseTree
        self.validTokens = []
        self.currentToken = self.tokens[self.index]

    # raise error for traceback
    def error(self):
        raise Exception('error with token: (' + self.currentToken.lexeme + ') at token index: ' + str(self.index))

    def getNextToken(self, node):
        # appends token to valid tokens
        self.validTokens.append(self.currentToken)
        node.tokens.append(self.currentToken.lexeme)
        if self.index < len(self.tokens) - 1:
            self.index += 1
        self.currentToken = self.tokens[self.index]

    def checkVarName(self):
        # checks valid name for vars
        if len(re.findall('[a-zA-Z_][a-zA-Z0-9_]*', self.currentToken.lexeme)) > 0:
            return re.findall('[a-zA-Z_][a-zA-Z0-9_]*', self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False

    # check real
    def checkInteger(self):
        if len(re.findall('[-+]?[0-9]*[.][0-9]+', self.currentToken.lexeme)) > 0:
            return re.findall('[-+]?[0-9]*[.][0-9]+', self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False

    # check natural
    def checkNaturalLiteral(self):
        if len(re.findall('[-+]?[0-9]+', self.currentToken.lexeme)) > 0:
            return re.findall('[-+]?[0-9]+', self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False

    # check bool
    def checkBoolean(self):
        booleanRegex = '((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|' + \
                             '(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))'

        if len(re.findall(booleanRegex, self.currentToken.lexeme)) > 0:
            return re.findall(booleanRegex, self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False

    # check char literal
    def checkCharacter(self):
        if len(re.findall("'\\\\?[ -~]'", self.currentToken.lexeme)) > 0:
            return re.findall("'\\\\?[ -~]'", self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False

    # check string literal
    def checkString(self):
        if len(re.findall("\'(\\\\.|[^\'\\\\])*\'", self.currentToken.lexeme)) > 0:
            return re.search("\'(\\\\.|[^\'\\\\])*\'", self.currentToken.lexeme)[0] == self.currentToken.lexeme
        return False



    # start parse
    def beginParsing(self, parent):

        parse = ParseTree("start", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse

        while self.currentToken.lexeme in ['{', 'if', 'while', 'String', 'int', 'char', 'float', 'bool', 'def'] or self.checkVarName() and self.index < len(self.tokens) - 1:
            self.statement(parse)


    def statement(self, parent):
        parse = ParseTree("statement", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse

       # check block
        if self.currentToken.lexeme == "{":
            self.block(parse)

        # check if
        elif self.currentToken.lexeme == "if":
            self.selection(parse)

        # check loop
        elif self.currentToken.lexeme == "while":
            self.whileLoop(parse)

        # check String
        elif self.currentToken.lexeme in ['String', 'int', 'char', 'float', 'bool', 'def']:
            self.declaration(parse)

        # check variable name
        elif self.checkVarName():
            self.assignment(parse)

        else:
            self.error()

    def block(self, parent):
        parse = ParseTree("block", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == "{":
            self.getNextToken(parse)
            self.beginParsing(parse)
            if self.currentToken.lexeme == '}':
                self.getNextToken(parse)
            else:
                self.error()
        else:
            self.error()

    def selection(self, parent):
        parse = ParseTree("selection", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == 'if':
            self.getNextToken(parse)
            if self.currentToken.lexeme == "(":
                self.getNextToken(parse)
                self.boolRelation(parse)
                if self.currentToken.lexeme == ")":
                    self.getNextToken(parse)
                    if self.currentToken.lexeme == "{":
                        self.getNextToken(parse)
                        self.beginParsing(parse)
                        if self.currentToken.lexeme == "}":
                            self.getNextToken(parse)
                            if self.currentToken.lexeme == "else":
                                self.elseStatement(parse)
                            elif self.currentToken.lexeme == "elif":
                                self.elifStatement(parse)
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def whileLoop(self, parent):
        parse = ParseTree("while_loop", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == "while":
            self.getNextToken(parse)
            if self.currentToken.lexeme == "(":
                self.getNextToken(parse)
                self.boolRelation(parse)
                if self.currentToken.lexeme == ")":
                    self.getNextToken(parse)
                    if self.currentToken.lexeme == "{":
                        self.getNextToken(parse)
                        self.beginParsing(parse)
                        if self.currentToken.lexeme == "}":
                            self.getNextToken(parse)
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def declaration(self, parent):

        parse = ParseTree("declaration", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme in ['String', 'int', 'char', 'float', 'bool']:
            self.variableDeclaration(parse)
        elif self.currentToken.lexeme == "def":
            self.functionDeclaration(parse)
       # print('Error')
        else:
            self.error()

    def assignment(self, parent):
        parse = ParseTree("assignment", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.checkVarName():
            self.getNextToken(parse)
            if self.currentToken.lexeme == '=':
                self.getNextToken(parse)
                self.boolRelation(parse)
        # print('Error here')
            else:
                self.error()
        else:
            self.error()

    def boolRelation(self, parent):
        parse = ParseTree("bool_relation", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        self.boolExpression(parse)
        while self.currentToken.lexeme in ['!==', '==']:
            self.getNextToken(parse)
            self.boolExpression(parse)

    def elseStatement(self, parent):

        parse = ParseTree("else_statement", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == "else":
            self.getNextToken(parse)
            if self.currentToken.lexeme == "{":
                self.getNextToken(parse)
                self.beginParsing(parse)
                if self.currentToken.lexeme == "}":
                    self.getNextToken(parse)
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def elifStatement(self, parent):
        parse = ParseTree("elif_statement", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == "elif":
            self.getNextToken(parse)
            if self.currentToken.lexeme == "(":
                self.getNextToken(parse)
                self.boolRelation(parse)
                if self.currentToken.lexeme == ")":
                    self.getNextToken(parse)
                    if self.currentToken.lexeme == "{":
                        self.getNextToken(parse)
                        self.beginParsing(parse)
                        if self.currentToken.lexeme == "}":
                            self.getNextToken(parse)
                            if self.currentToken.lexeme == "else":
                                self.elseStatement(parse)
                            elif self.currentToken.lexeme == "elif":
                                self.elifStatement(parse)
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def variableDeclaration(self, parent):
        parse = ParseTree("var_declare", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme in ['String', 'int', 'char', 'float', 'bool']:
            self.getNextToken(parse)
            if self.checkVarName():
                self.getNextToken(parse)
            else:
                self.error()
        else:
            self.error()

    def functionDeclaration(self, parent):
        parse = ParseTree("func_declare", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.currentToken.lexeme == "def":
            self.getNextToken(parse)
            if self.checkVarName():
                self.getNextToken(parse)
                if self.currentToken.lexeme == "(":
                    self.getNextToken(parse)
                    while self.checkVarName():
                        self.getNextToken(parse)
                        if self.currentToken.lexeme == ',':
                            self.getNextToken(parse)
                        else:
                            self.error()
                    if self.currentToken.lexeme == ')':
                        self.getNextToken(parse)
                        if self.currentToken.lexeme == "{":
                            self.getNextToken(parse)
                            self.beginParsing(parse)
                            if self.currentToken.lexeme == "}":
                                self.getNextToken(parse)
                            else:
                                self.error()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def boolExpression(self, parent):

        parse = ParseTree("bool_expr", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        self.expr(parse)
        while self.currentToken.lexeme in ['<==', '>==', '<', '>']:
            self.getNextToken(parse)
            self.expr(parse)

    def expr(self, parent):

        parse = ParseTree("expr", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse= parse
        self.term(parse)
        while self.currentToken.lexeme in ['+', '-']:
            self.getNextToken(parse)
            self.term(parse)

    def term(self, parent):
        parse = ParseTree("term", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        self.exp(parse)
        while self.currentToken.lexeme in ['*', '/', '%']:
            self.getNextToken(parse)
            self.exp(parse)

    def exp(self, parent):
        parse = ParseTree("exp", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        self.logical(parse)
        while self.currentToken.lexeme == '^':
            self.getNextToken(parse)
            self.logical(parse)

    def logical(self, parent):
        parse = ParseTree("logical", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse

        self.factor(parse)
        while self.currentToken.lexeme in ['~', '&', '|']:
            self.getNextToken(parse)
            self.factor(parse)

    # def fac
    def factor(self, parent):
        parse = ParseTree("factor", [self.currentToken.lexeme])
        parent.add_child(parse)
        self.currentParse = parse
        if self.checkInteger() or self.checkNaturalLiteral() or self.checkBoolean() or self.checkCharacter() or self.checkString() or self.currentToken.lexeme in ['!', '~']:
            if self.currentToken.lexeme in ['!', '~']:
                self.getNextToken(parse)
            self.getNextToken(parse)
        elif self.currentToken.lexeme == "(":
            self.getNextToken(parse)
            self.boolRelation(parse)
            if self.currentToken.lexeme == ")":
                self.getNextToken(parse)
            else:
                self.error()
        elif self.checkVarName() or self.currentToken.lexeme in ['-', '+']:
            if self.currentToken.lexeme in ['-', '+']:
                self.getNextToken(parse)
            self.getNextToken(parse)
            if self.currentToken.lexeme == "(":
                self.getNextToken(parse)
                while self.checkVarName():
                    self.getNextToken(parse)
                    if self.currentToken.lexeme == ',':
                        self.getNextToken(parse)
                    else:
                        self.error()
                if self.currentToken.lexeme == ")":
                    self.getNextToken(parse)
                else:
                    self.error()
        else:
            self.error()