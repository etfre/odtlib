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

def get_styles(self, content):
    '''
    Return a list of style wrappers.
    '''
    stylelist = []
    for styles in content.iterchildren():
        if styles.tag in [qn('office', 'automatic-styles'), qn('office', 'styles')]:
            # xml parsing is never pretty
            for s in styles.iterchildren(qn('style', 'style')):
                for k, v in s.attrib.items():
                    prefix = shared.get_prefix(k)
                    tag = shared.get_tag(k)
                    if tag == 'name': name = v
                    if tag == 'family': family = v
                attribs = s.find(qn('style', 'text-properties')).attrib
                stylelist.append(style.Style(s, name, family, attribs))
    return stylelist

def make_span(text, style_name):
    return shared.makeelement('text', 'span', text,
                              {qn('text', 'style-name'): style_name})