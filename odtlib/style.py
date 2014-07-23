from odtlib.utilities import shared
from odtlib import constants

from odtlib.namespace import NSMAP, qn, qn22
from copy import deepcopy

class Style:
    def __init__(self, name, family):
        assert isinstance(name, str)
        self._ele = shared.makeelement('style', 'style')
        self._ele.append(shared.makeelement('style', 'text-properties'))
        self._ele.set(qn22('style:name'), name)
        self._ele.set(qn22('style:family'), family)

    @classmethod
    def _from_element(cls, ele):
        name = ele.attrib[qn22('style:name')]
        family = ele.attrib[qn22('style:family')]
        style = cls(name, family)
        style._ele = ele
        return style

    @property
    def name(self):
        return self._ele.get(qn22('style:name'))

    @name.setter
    def name(self, value):
        self._ele.set(qn22('style:name'), value)

    @property
    def family(self):
        return self._ele.get(qn22('style:family'))

    @family.setter
    def family(self, value):
        self._ele.set(qn22('style:family'), value)

    @property
    def bold(self):
        return self._get_property('bold')

    @bold.setter
    def bold(self, value):
        self._set_property(value, 'bold')

    @property
    def italic(self):
        return self._get_property('italic')

    @italic.setter
    def italic(self, value):
        self._set_property(value, 'italic')

    @property
    def color(self):
        return self._get_property('color')

    @color.setter
    def color(self, value):
        self._set_property(value, 'color')

    def _get_property(self, prop):
        tprops = self._ele.find(qn22('style:text-properties'))
        for i, attrconstant in enumerate(constants.STYLE_ATTRIBUTES[prop]):
            if i == 0:
                first_value = tprops.get(attrconstant)
            if tprops.get(attrconstant) is None:
                return None
            if tprops.get(attrconstant) != first_value:
                return None
        # Inverse dict lookup because we're sharing this constant dict with the Style class
        for key in constants.PROPERTY_INPUT_MAP[prop]:
            if constants.PROPERTY_INPUT_MAP[prop][key] == first_value:
                return key
        return first_value

    def _set_property(self, value, prop):
        prop_dict = constants.PROPERTY_INPUT_MAP[prop]
        tprops = self._ele.find(qn22('style:text-properties'))
        for attr in constants.STYLE_ATTRIBUTES[prop]:
            if value is None:
                if attr in tprops.attrib:
                    del tprops.attrib[attr]
                continue
            # If prop_dict is empty, we simply set every attribute to value
            # Used for strings like RGB colors
            if not prop_dict:
                if not isinstance(value, str):
                    raise ValueError("{} property must be a string or None".format(prop))
                tprops.set(attr, value)
                continue
            try:
                tprops.set(attr, prop_dict[value])
            except KeyError:
                raise ValueError("Invalid value {} for {} property".format(value, prop))

def matches_attributes(value, element, attributes):
    '''
    Given an lxml element, a value, and a list of properties,
    return whether all of the given element attributes match the value argument
    '''
    for attribute in attributes:
        if attribute not in element.attrib or element.get(attribute) != value:
            return False
    return True

def build_styles_dict(styles_elements):
    '''
    Return a list of style wrappers. Create an <office:styles>
    element if one does not already exist.
    '''
    styledict = {}
    for styles in styles_elements.values():
        for s in styles.iterchildren(qn22('style:style')):
            wrapper = Style._from_element(s)
            styledict[wrapper.name] = wrapper
    return styledict

def add_standard_styles(ele):
    pass

def get_family(wrapper):
    if wrapper._ele.tag == qn22('text:p'):
        return 'paragraph'
    if wrapper._ele.tag == qn22('text:h'):
        return 'paragraph'
    if wrapper._ele.tag == qn22('text:span'):
        return 'text'

def get_name(family, styles):
    letter = ''
    if family:
        letter = family[0].upper()
    num = 1
    name = '{}{}'.format(letter, num)
    while name in [s.get(qn22('style:name')) for s in styles]:
        num += 1
        name = '{}{}'.format(letter, num)
    return name

def make_empty_style():
    s = shared.makeelement('style', 'style')
    s.append(shared.makeelement('style', 'text-properties'))
    return s