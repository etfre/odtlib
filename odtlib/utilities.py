import zipfile
import os
import re
import collections
from lxml import etree
from odtlib.namespace import NSMAP, qn

def load_xml_files(folder):
    xmlfiles = {}
    for root, dirs, files in os.walk(folder):
        for filename in files:
            abspath = os.path.join(root, filename)
            relpath = os.path.relpath(abspath, folder)
            try:
                with open(abspath) as f:
                    xmlfile = (etree.fromstring(f.read().encode('utf_8')))
                    xmlfiles[relpath] = xmlfile
            except (UnicodeDecodeError, etree.XMLSyntaxError):
                pass
    return xmlfiles

def write_xml_files(xmlfiles, folder):
    for filename, element in xmlfiles.items():
        abspath = os.path.join(folder, filename)
        with open(abspath, 'w') as f:
            f.write(etree.tostring(element, xml_declaration=True).decode(encoding='UTF-8'))

def makeelement(prefix, tagname, text='', attributes={}):
    namespace = qn(prefix, tagname)
    newelement = etree.Element(namespace, nsmap=NSMAP)
    for k, v in attributes.items():
        try:
            newelement.set(k, v)
        except ValueError:
            spl = k.split(':')
            newelement.set(qn(spl[0], spl[1]), v)
    if text: newelement.text = text
    return newelement

def remove_children(element, tag=None):
    for child in element.iterchildren():
        element.remove(child)

def remove_substr(start, end, mystr):
    assert end >= start
    return ''.join([mystr[:start], mystr[end:]])

def insert_substr(start, substr, mystr):
    assert start >= 0
    return ''.join([mystr[:start], substr, mystr[start:]])

def contains_match_start(start, end, match_slices):
    '''
    Test whether at least one match begins within the scope of an element
    text boundaries
    '''
    for slice in match_slices:
        if start <= slice[0] < end:
            return True
    return False

def lies_within_match(start, end, match_slices):
    '''
    Test whether entire an element text lies entirely within a match
    '''
    for slice in match_slices:
        if start >= slice[0] and slice[1] >= end:
            return True
    return False

def create_replace_dict(para, slices):
    eledict = collections.OrderedDict()
    start = 0
    if para.text is not None:
        eledict[para] =  [start, len(para.text)]
        start += len(para.text)
    span_list = para.findall(qn('text', 'span'))
    for i, span in enumerate(span_list):
        if lies_within_match(start, start + len(span.text), slices):
            prev = list(eledict.keys())[-1]
            prev.text += span.text
            eledict[prev][1] += len(span.text)
            para.remove(span)
        else:
            eledict[span] = [start, start + len(span.text)]
        start += len(span.text)
        # OpenDocument treats text that matches the style of the containing paragraph
        # as part of that paragraph's text property, regardless of where it is in
        # the paragraph. We can find these pieces of text by checking the tail of
        # each span element. Then clear the span's tail, and place the text in a
        # placeholder element for use in the replace method
        if span.tail is not None:
            if lies_within_match(start, start + len(span.text), slices):
                prev = list(eledict.keys())[-1]
                prev.text += span.tail
                eledict[prev][1] += len(span.tail)
            else:
                placeholder = makeelement('text', 'placeholder', span.tail)
                eledict[placeholder] = [start, start + len(span.tail)]
            start += len(span.tail)
            span.tail = None
    return eledict

def merge_placeholders(eledict):
    for i, (ele, info) in enumerate(eledict.items()):
        if ele.tag == qn('text', 'placeholder'):
            if list(eledict.items())[i-1][0].tail is None: list(eledict.items())[i-1][0].tail = ''
            list(eledict.items())[i-1][0].tail += ele.text

def get_tag(namespace):
    return re.match(r'{[^}]*}(\S+)', namespace).group(1)

def get_prefix(namespace):
    return re.match(r'{([^}]*)}', namespace).group(1)
















