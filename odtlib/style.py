from odtlib.utilities import shared
from odtlib.constants.styleattribs import STYLE_ATTRIBUTES, BASE_STYLE_PROPERTIES

from odtlib.namespace import NSMAP, qn
from copy import deepcopy

class Style:
    def __init__(self, name, family):
        self._ele = shared.makeelement('style', 'style')
        self._ele.append(shared.makeelement('style', 'text-properties'))
        self.name = name
        self.family = family
        self._style_properties = BASE_STYLE_PROPERTIES.copy()

    @classmethod
    def _from_element(cls, ele):
        name = ele.attrib[qn('style', 'name')]
        family = ele.attrib[qn('style', 'family')]
        style = cls(name, family)
        style._ele = ele
        style._style_properties = set_style_properties(style._ele.find(qn('style', 'text-properties')))
        return style

    @property
    def bold(self):
        return self._style_properties['bold']

    @bold.setter
    def bold(self, value):
        textutilities.set_property(self, 'bold', value)

    @property
    def italic(self):
        return self._style_properties['italic']

    @italic.setter
    def italic(self, value):
        textutilities.set_property(self, 'italic', value)

def set_style_properties(text_properties):
    sprops = {}
    sprops['bold'] = set_bool_property('bold', text_properties)
    sprops['italic'] = set_bool_property('italic', text_properties)
    return sprops

def set_bool_property(prop, text_properties):
    '''
    Based on the attributes of a <style: text-properties> element,
    set the 
    '''
    for attribute in STYLE_ATTRIBUTES[prop]:
        if text_properties.get(attribute) != prop:
            return False
    return True



def build_styles_list(automatic, office):
    '''
    Return a list of style wrappers. Create an <office: styles>
    element if one does not already exist.
    '''
    stylelist = []
    for styles in [automatic, office]:
        for s in styles.iterchildren(qn('style', 'style')):
            stylelist.append(Style._from_element(s))
    return stylelist

def update_style(wrapper, automatic_styles, office_styles):
    '''
    From the properties of the wrapper object, build
    a <style:style> element. If that style's attributes
    do not match those of another style in <office:automatic-styles>
    or <office:styles>, append the style to <office:styles>
    '''
    styles = deepcopy(list(automatic_styles) + list(office_styles))
    family = get_family(wrapper)
    name = get_name(family, styles)
    style = shared.makeelement('style', 'style', attributes=
        {qn('style', 'name'): name, qn('style', 'family'): family})
    properties = shared.makeelement('style', 'text-properties')
    style.append(properties)
    set_properties(wrapper, properties)
    for s in styles:
        if (s.get(qn('style', 'family')) == family and
        s.find(qn('style', 'text-properties')).attrib == properties):
            wrapper.style = s.get(qn('style', 'name'))
            return
    wrapper.style = name
    office_styles.append(style)

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
    while name in [style.get(qn('style', 'name')) for style in styles]:
        num += 1
        name = '{}{}'.format(letter, num)
    return name

# def set_properties(wrapper, properties):
#     set_bool_property(wrapper.bold, 'bold', properties, styleattribs.BOLD_ATTRIBUTES)
    # if wrapper.bold is True:
    #     for prop in styleattribs.BOLD_ATTRIBUTES:
    #         properties.set(prop, 'bold')
    # else:
    #     for prop in styleattribs.BOLD_ATTRIBUTES:
    #         properties.set(prop, 'normal')

# def set_bool_property(wrapper_prop, true_value, properties, attr_constants, false_value='normal'):
#     for prop in attr_constants:
#         if wrapper_prop is True:
#             properties.set(prop, true_value)
#         else:
#             properties.set(prop, false_value)


