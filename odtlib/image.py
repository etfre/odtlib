from odtlib.namespace import NSMAP, qn
from odtlib.utilities import shared, imageutilities

class Image:
	def __init__(self, filename, width='0', height='0'):
		self._ele = shared.makeelement('text', 'p', attributes={qn('text:style-name'): 'Standard'})
		