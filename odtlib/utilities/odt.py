from copy import deepcopy
from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn
from odtlib import style

def convert_to_spans(text_parent):
    '''
    Convert all paragraph text to spans for easier API handling.
    This will be reversed when the document is saved.
    '''
    for para in text_parent.iterchildren(qn('text', 'p')):
        new_list = []
        style_name = shared.get_style_name(para)
        attributes = deepcopy(para.attrib)
        if para.text:
            new_list.append(make_span(para.text, style_name))
        for i, span in enumerate(para.iterchildren(qn('text', 'span'))):
            new_list.append(span)
            if span.tail is not None:
                new_list.append(make_span(span.tail, style_name))
                span.tail = None
        para.clear()
        for span in new_list:
            para.append(span)
        for attr, value in attributes.items():
            para.set(attr, value)

def convert_from_spans(text_parent):
    for para in text_parent.iterchildren(qn('text', 'p')):
        new_list = []
        para_style = shared.get_style_name(para)
        attributes = deepcopy(para.attrib)
        previous = None
        paratext = ''
        for i, span in enumerate(para.iterchildren(qn('text', 'span'))):
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
        for span in new_list:
            para.append(span)
        for attr, value in attributes.items():
            para.set(attr, value)

def make_span(text, style_name):
    return shared.makeelement('text', 'span', text,
                              {qn('text', 'style-name'): style_name})