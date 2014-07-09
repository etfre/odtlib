import re
from odtlib.utilities import shared, textutilities
from odtlib.lists import baselist
from odtlib.namespace import NSMAP, qn
from odtlib.constants.styleattribs import BASE_STYLE_PROPERTIES
from odtlib import style

class BaseText:
    def __init__(self, style):
        self._style = style
        self._style_properties = BASE_STYLE_PROPERTIES.copy()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value
        if value is None:
            self._ele.attrib.pop(qn('text', 'style-name'), None)
            return
        try:
            self._ele.set(qn('text', 'style-name'), value.name)
        except AttributeError:
            self._ele.set(qn('text', 'style-name'), value)

    @property
    def bold(self):
        return self._style_properties['bold']

    @bold.setter
    def bold(self, value):
        textutilities.set_property(self, 'bold', value)

    @property
    def italics(self):
        return self._style_properties['italics']

    @italics.setter
    def italics(self, value):
        textutilities.set_property(self, 'italics', value)

    
