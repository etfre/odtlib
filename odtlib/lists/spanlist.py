from odtlib.lists import baselist
from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn

class SpanList(baselist.ElementList):
    def __init__(self, parent, data=[]):
        super().__init__(parent, data)