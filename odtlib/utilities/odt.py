import copy
from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn
from odtlib import style

def convert_to_spans(ele):
    '''
    Convert paragraph text to spans for easier API handling.
    This will be reversed by convert_from_spans when the document is saved.
    '''
    new_list = []
    style_name = ele.get(qn('text:style-name'))
    attributes = copy.deepcopy(ele.attrib)
    if ele.text:
        new_list.append(make_span(ele.text, style_name))
    for child in ele.iterchildren():
        new_list.append(child)
        if child.tail is not None:
            new_list.append(make_span(child.tail, style_name))
            child.tail = None
    ele.clear()
    ele.extend(new_list)
    for attr, value in attributes.items():
        ele.set(attr, value)


def convert_from_spans(ele):
    '''
    Every span with a style matching the style of its containing
    paragraph is removed, and its text becomes part of the paragaph's
    text.
    '''
    new_list = []
    ele_style = ele.get(qn('text:style-name'))
    attributes = copy.deepcopy(ele.attrib)
    previous = None
    paratext = ''
    for child in ele.iterchildren():
        child_style = shared.get_style_name(child)
        if ele_style == child_style:
            if previous == None:
                paratext += child.text
            else:
                previous.tail = child.text
        else:
            new_list.append(child)
            previous = child
    ele.clear()
    if paratext:
        ele.text = paratext
    ele.extend(new_list)
    for attr, value in attributes.items():
        ele.set(attr, value)

def get_style_containers(content, styles_file):
    '''
    Return <office: automatic-styles> and <office: styles> elements. Create
    these elements and add them as children of <office:document-content> if
    they do not already exist.
    '''
    styles_dict = {
        'automatic': content.find(qn('office:automatic-styles')),
        'other': content.find(qn('office:styles')),
        'stylefile office': styles_file.find(qn('office:styles')),
    }
    if styles_dict['automatic'] is None:
        styles_dict['automatic'] = shared.makeelement('office', 'automatic-styles')
        content.insert(0, styles_dict['automatic'])
    if styles_dict['other'] is None:
        styles_dict['other'] = shared.makeelement('office', 'styles')
        styles_dict['automatic'].addnext(styles_dict['other'])
    if styles_dict['stylefile office'] is None:
        styles_dict['stylefile office'] = shared.makeelement('office', 'styles')
        styles_file.append(styles_dict['stylefile office'])
    return styles_dict

def make_span(text, style_name):
    '''
    Given text and a style name, create and return a <text:span> element
    '''
    try:
        return shared.makeelement('text', 'span', text,
            {qn('text:style-name'): style_name})
    except TypeError:
        return shared.makeelement('text', 'span', text)

def get_default_styles(root):
    wrappers = {}
    for s in root.find(qn('office:styles')).iterchildren(qn('style:style')):
        wrapper = style.Style._from_element(s)
        wrappers[wrapper.name] = wrapper
    return wrappers







