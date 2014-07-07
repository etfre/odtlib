import re
from odtlib.utilities import shared, texthelpers
from odtlib.lists import baselist
from odtlib.namespace import NSMAP, qn

class BaseText:
    def __init__(self, style):
        self._style = style

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value
        try:
            self._ele.set(qn('text', 'style-name'), value.name)
        except AttributeError:
            self._ele.set(qn('text', 'style-name'), value)