from copy import deepcopy
from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn, qn22
from odtlib import style

def convert_to_spans(text_parent):
    '''
    Convert all paragraph text to spans for easier API handling.
    This will be reversed by convert_from_spans when the document is saved.
    '''
    for para in text_parent.iterchildren():
        if para.tag in [qn22('text:p'), qn22('text:h')]:
            new_list = []
            style_name = shared.get_style_name(para)
            attributes = deepcopy(para.attrib)
            if para.text:
                new_list.append(make_span(para.text, style_name))
            for span in para.iterchildren(qn22('text:span')):
                new_list.append(span)
                if span.tail is not None:
                    new_list.append(make_span(span.tail, style_name))
                    span.tail = None
            para.clear()
            para.extend(new_list)
            for attr, value in attributes.items():
                para.set(attr, value)

def convert_from_spans(text_parent):
    '''
    Every span with a style matching the style of its containing
    paragraph is removed, and its text becomes part of the paragaph's
    text.
    '''
    for para in text_parent.iterchildren():
        if para.tag in [qn22('text:p'), qn22('text:h')]:
            new_list = []
            para_style = shared.get_style_name(para)
            attributes = deepcopy(para.attrib)
            previous = None
            paratext = ''
            for span in para.iterchildren(qn22('text:span')):
                span_style = shared.get_style_name(span)
                if para_style == span_style:
                    if previous == None:
                        paratext += span.text
                    else:
                        previous.tail = span.text
                else:
                    new_list.append(span)
                    previous = span
            para.clear()
            if len(paratext):
                para.text = paratext
            para.extend(new_list)
            for attr, value in attributes.items():
                para.set(attr, value)

def get_style_containers(content, styles_file):
    '''
    Return <office: automatic-styles> and <office: styles> elements. Create
    these elements and add them as children of <office:document-content> if
    they do not already exist.
    '''
    styles_dict = {
        'automatic': content.find(qn22('office:automatic-styles')),
        'other': content.find(qn22('office:styles')),
        'stylefile office': styles_file.find(qn22('office:styles')),
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
    return shared.makeelement('text', 'span', text,
                              {qn22('text:style-name'): style_name})

def get_default_styles(root):
    wrappers = {}
    for s in root.find(qn22('office:styles')).iterchildren(qn22('style:style')):
        wrapper = style.Style._from_element(s)
        wrappers[wrapper.name] = wrapper
    return wrappers







