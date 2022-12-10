from Parser import Parser
from Lexer import Lexer


class Compiler:
	def __init__(self, file):
		# takes in an INPUT FILE and converts it to one input str
		self.code = file.read()
		lexer = Lexer(self.code)
		if lexer.tokenizer():
			tokens = lexer.tokens
			#print('Tokens: ',tokens)
			if len(tokens) > 0:
				parser = Parser(tokens)
				parser.beginParsing(parser.parseTree)
				parser.parseTree.printParseTree()
		else:
			print("Unrecognized Lexeme at index {:2d} is invalid\n".format(len(lexer.tokens)))