from odtlib.utilities import shared
from odtlib.constants.styleattribs import STYLE_ATTRIBUTES, BASE_STYLE_PROPERTIES, PROPERTY_INPUT_MAP

from odtlib.namespace import NSMAP, qn
from copy import deepcopy

class Style:
    def __init__(self, name, family):
        assert isinstance(name, str)
        self._ele = shared.makeelement('style', 'style')
        self._props_dict = {'text': shared.makeelement('style', 'text-properties')}
        self._ele.append(self._props_dict['text'])
        self._ele.set(qn('style', 'name'), name)
        self._ele.set(qn('style', 'family'), family)
        self._style_properties = BASE_STYLE_PROPERTIES.copy()

    @classmethod
    def _from_element(cls, ele):
        name = ele.attrib[qn('style', 'name')]
        family = ele.attrib[qn('style', 'family')]
        style = cls(name, family)
        style._ele = ele
        style._props_dict = {'text': style._ele.find(qn('style', 'text-properties'))}
        style._style_properties = initiate_style_properties(style._props_dict, style._style_properties)
        return style

    @property
    def name(self):
        return self._ele.get(qn('style', 'name'))

    @name.setter
    def name(self, value):
        self._ele.set(qn('style', 'name'), value)

    @property
    def family(self):
        return self._ele.get(qn('style', 'family'))

    @family.setter
    def family(self, value):
        self._ele.set(qn('style', 'family'), value)

    @property
    def bold(self):
        return self._style_properties['bold']

    @bold.setter
    def bold(self, value):
        self._set_property(value, 'bold')

    @property
    def italic(self):
        return self._style_properties['italic']

    @italic.setter
    def italic(self, value):
        self._set_property(value, 'italic')

    @property
    def color(self):
        return self._style_properties['color']

    @color.setter
    def color(self, value):
        self._set_property(value, 'color')

    def _set_property(self, value, prop):
        prop_dict = PROPERTY_INPUT_MAP[prop]
        for attr in STYLE_ATTRIBUTES[prop]:
            if value is None:
                if attr in self._props_dict['text'].attrib:
                    del self._props_dict['text'].attrib[attr]
                continue
            # If prop_dict is empty, we simply set every attribute to value
            # Used for strings like RGB colors
            if not prop_dict:
                if not isinstance(value, str):
                    raise ValueError("{} property must be a string or None".format(prop))
                self._props_dict['text'].set(attr, value)
                continue
            try:
                self._props_dict['text'].set(attr, prop_dict[value])
            except KeyError:
                raise ValueError("Invalid value {} for {} property".format(value, prop))
        self._style_properties[prop] = value

def initiate_style_properties(props_dict, sprops):
    if props_dict['text'] is not None:
        if matches_attributes('bold', props_dict['text'], STYLE_ATTRIBUTES['bold']):
            sprops['bold'] = True
        if matches_attributes('italic', props_dict['text'], STYLE_ATTRIBUTES['italic']):
            sprops['italic'] = True
        if props_dict['text'].get(qn('fo', 'color')) is not None:
            sprops['color'] = props_dict['text'].get(qn('fo', 'color'))
    return sprops

def matches_attributes(value, element, attributes):
    '''
    Given an lxml element, a value, and a list of properties,
    return whether all of the given element attributes match the value argument
    '''
    for attribute in attributes:
        if attribute not in element.attrib or element.get(attribute) != value:
            return False
    return True

def build_styles_dict(automatic, office):
    '''
    Return a list of style wrappers. Create an <office: styles>
    element if one does not already exist.
    '''
    styledict = {}
    for styles in [automatic, office]:
        for s in styles.iterchildren(qn('style', 'style')):
            wrapper = Style._from_element(s)
            styledict[wrapper.name] = wrapper
    return styledict

def get_family(wrapper):
    if wrapper._ele.tag == qn('text', 'p'):
        return 'paragraph'
    if wrapper._ele.tag == qn('text', 'span'):
        return 'text'

def get_name(family, styles):
    letter = ''
    if family:
        letter = family[0].upper()
    num = 1
    name = '{}{}'.format(letter, num)
    while name in [s.get(qn('style', 'name')) for s in styles]:
        num += 1
        name = '{}{}'.format(letter, num)
    return name

def make_empty_style():
    s = shared.makeelement('style', 'style')
    s.append(shared.makeelement('style', 'text-properties'))
    return s