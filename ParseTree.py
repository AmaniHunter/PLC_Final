class ParseTree:
	def __init__(self, name = "", tokens = []):
		self.name = name
		self.tokens = tokens
		self.children = []
		self.parent = None

	def add_child(self, child):
		self.child = child
		child.parent = self
		self.children.append(child)

	# return depth of node
	def get_depth(self):
		depth = 0
		p = self.parent
		while p:
			p = p.parent
			depth += 1
		return depth

	# displays tree
	def printParseTree(self):
		print(' ' * self.get_depth(), end='')
		t_list = ""
		#generic
		if len(self.tokens[1:]) > 0:
			t_list += " - tokens validated: " + ', '.join(self.tokens[1:])
		print("Function ", self.name ,  t_list)
		if self.children:
			for child in self.children:
				child.printParseTree()
