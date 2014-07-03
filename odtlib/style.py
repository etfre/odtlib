class Style:
	def __init__(self, name, family, attributes={}):
		self._ele = None
		self.name = name
		self.family = family
		self.attributes = attributes

	@classmethod
	def _from_element(cls, ele):
		style = cls(1, 2, 3)
		style._ele = ele
		return ele