import zipfile
import os
import re
import collections
import copy
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
    spans_to_remove = []
    for span in para.spans:
        if lies_within_match(start, start + len(span.text), slices):
            prev = list(eledict.keys())[-1]
            prev.text += span.text
            eledict[prev][1] += len(span.text)
            spans_to_remove.append(span)
        else:
            eledict[span] = [start, start + len(span.text)]
        start += len(span.text)
    for span in spans_to_remove:
        para.spans.remove(span)
    return eledict

def get_tag(namespace):
    return re.match(r'{[^}]*}(\S+)', namespace).group(1)

def get_prefix(namespace):
    return re.match(r'{([^}]*)}', namespace).group(1)

def get_default_paragraph_style_name(doc):
    auto = doc.find(qn('office', 'automatic-styles'))
    for child in auto.iterchildren(qn('style', 'style')):
        if (set((qn('style', 'family'), qn('style', 'name'))) <= set(child.attrib) and
        child.attrib[qn('style', 'family')] == 'paragraph'):
            return child.attrib[qn('style', 'name')]
    return None

def get_paragraph_text(ele):
    textlist = []
    if ele.text is not None:
        textlist.append(ele.text)
    for span in ele.iter(qn('text', 'span')):
        if span.text is not None:
            textlist.append(span.text)
        if span.tail is not None:
            textlist.append(span.tail)
    return ''.join(textlist)

def get_style_name(element):
    '''
    Given a <text:p> or <text:span> element, return a string
    indicating the name of the associated style element
    '''
    assert element.tag in [qn('text', 'p'), qn('text', 'span')]
    for attribute, value in element.attrib.items():
        if attribute == qn('text', 'style-name'): return value

def get_or_make_child(ele, prefix, tag):
    child = ele.find(qn(prefix, tag))
    if child is None:
        child = makeelement(prefix, tag)
        ele.append(child) 
    return child

def compare_elements(a, b, attributes_to_exclude=[]):
    if not isinstance(attributes_to_exclude, list):
        attributes_to_exclude = [attributes_to_exclude]
    a_copy = copy.deepcopy(a)
    b_copy = copy.deepcopy(b)
    for attr in attributes_to_exclude:
        if attr in a_copy.attrib:
            del a_copy.attrib[attr]
        if attr in b_copy.attrib:
            del b_copy.attrib[attr]
    if ([a_copy.tag, a_copy.tail, a_copy.text, a_copy.attrib, len(list(a_copy))] !=
        [b_copy.tag, b_copy.tail, b_copy.text, b_copy.attrib, len(list(b_copy))]):
        return False
    equivalent_children = []
    for i, a_child in enumerate(a.iterchildren(), start=1):
        for b_child in b.iterchildren():
            if (b_child not in equivalent_children and
                compare_elements(a_child, b_child, attributes_to_exclude)):
                equivalent_children.append(b_child)
                break
    if len(equivalent_children) != len(list(a_copy)):
        return False
    return True


