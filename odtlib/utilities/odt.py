from copy import deepcopy
from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn
from odtlib import style

def convert_to_spans(text_parent):
    '''
    Convert all paragraph text to spans for easier API handling.
    This will be reversed by convert_from_spans when the document is saved.
    '''
    for para in text_parent.iterchildren(qn('text', 'p')):
        new_list = []
        style_name = shared.get_style_name(para)
        attributes = deepcopy(para.attrib)
        if para.text:
            new_list.append(make_span(para.text, style_name))
        for span in para.iterchildren(qn('text', 'span')):
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
    for para in text_parent.iterchildren(qn('text', 'p')):
        new_list = []
        para_style = shared.get_style_name(para)
        attributes = deepcopy(para.attrib)
        previous = None
        paratext = ''
        for span in para.iterchildren(qn('text', 'span')):
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

def get_style_containers(content):
    '''
    Return <office: automatic-styles> and <office: styles> elements. Create
    these elements and add them as children of <office:document-content> if
    they do not already exist.
    '''
    automatic = content.find(qn('office', 'automatic-styles'))
    other = content.find(qn('office', 'styles'))
    if automatic is None:
        automatic = shared.makeelement('office', 'automatic-styles')
        content.insert(0, automatic)
    if other is None:
        other = shared.makeelement('office', 'styles')
        automatic.addnext(other)
    return automatic, other

def make_span(text, style_name):
    '''
    Given text and a style name, create and return a <text:span> element
    '''
    return shared.makeelement('text', 'span', text,
                              {qn('text', 'style-name'): style_name})








