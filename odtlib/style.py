from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn

class Style:
    def __init__(self, name, family):
        self._ele = shared.makeelement('style', 'style')
        self.name = name
        self.family = family

    @classmethod
    def _from_element(cls, ele):
        name = ele.attrib[qn('style', 'name')]
        family = ele.attrib[qn('style', 'family')]
        style = cls(name, family)
        style._ele = ele
        return style

def build_styles_list(content):
    '''
    Return a list of style wrappers.
    '''
    stylelist = []
    for styles in content.iterchildren():
        if styles.tag in [qn('office', 'automatic-styles'), qn('office', 'styles')]:
            for s in styles.iterchildren(qn('style', 'style')):
                stylelist.append(Style._from_element(s))
    return stylelist

def update_style(wrapper):
    if wrapper.style is not None:
        return
    # automatic = content.find(qn('office', 'automatic-styles'))
    # other = content.find(qn('office', 'styles'))
    # if other is None:
    #     other = shared.makeelement('office', 'styles')
    #     if automatic is not None:
    #         automatic.addnext(other)
    #     else:
    #         content.insert(0, other)
    # for wrapper in style_wrappers:
    #     if automatic is None or wrapper.name in [s.attrib[qn('style', 'name')] for s in automatic]:
    #         continue
    #     if wrapper.name not in [s.attrib[qn('style', 'name')] for s in other]:
    #         other.append(wrapper._ele)

def get_style_properties(ele):
    '''
    Return a dictionary of style properties from a <style:style> element
    for use in the Style wrapper
    '''