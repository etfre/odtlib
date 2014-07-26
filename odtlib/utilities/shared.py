import zipfile
import os
import re
import collections
import copy
from lxml import etree
from odtlib.namespace import NSMAP, qn

def load_xml_files(folder):
    '''
    Create and return dictionary that maps relative paths of
    all xml-parsable files in a folder with a corresponding lxml
    element

    Args:
        folder: String path of a folder
    Returns:
        Dictionary with relative path/element mappings
    '''
    xmlfiles = {}
    for root, dirs, files in os.walk(folder):
        for filename in files:
            abspath = os.path.join(root, filename)
            try:
                with open(abspath) as f:
                    xmlfile = (etree.fromstring(f.read().encode('utf_8')))
                    xmlfiles[os.path.relpath(abspath, folder)] = xmlfile
            except (UnicodeDecodeError, etree.XMLSyntaxError):
                pass
    return xmlfiles

def write_xml_files(xmlfiles, folder):
    '''
    Write a dictionary of lxml elements to files in a folder

    Args:
        xmlfiles: Dictionary with relative path/element mappings
        folder: String path of a folder to which the elements in
            xmlfiles will be copied
    '''
    for filename, element in xmlfiles.items():
        abspath = os.path.join(folder, filename)
        with open(abspath, 'w') as f:
            f.write(etree.tostring(element, xml_declaration=True).decode(encoding='UTF-8'))

def makeelement(prefix, tagname, text='', attributes=None):
    if attributes is None:
        attributes = {}
    namespace = qn('{}:{}'.format(prefix, tagname))
    newelement = etree.Element(namespace, nsmap=NSMAP)
    for k, v in attributes.items():
        try:
            newelement.set(k, v)
        except ValueError:
            newelement.set(qn(k), v)
    if text: newelement.text = text
    return newelement

def remove_children(element, tag=None):
    for child in element.iterchildren(tag):
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
    for s in match_slices:
        if start <= s[0] < end:
            return True
    return False

def lies_within_match(start, end, match_slices):
    '''
    Test whether entire an element text lies entirely within a match
    '''
    for s in match_slices:
        if start >= s[0] and s[1] >= end:
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

def get_style_name(element):
    '''
    Given a <text:p> or <text:span> element, return a string
    indicating the name of the associated style element
    '''
    assert element.tag in [qn('text:h'), qn('text:p'), qn('text:span')]
    return element.get(qn('text:style-name'))
    # for attribute, value in element.attrib.items():
    #     if attribute == qn('text:style-name'): return value

def get_or_make_child(ele, prefix, tag):
    child = ele.find(qn('{}:{}'.format(prefix, tag)))
    if child is None:
        child = makeelement(prefix, tag)
        ele.append(child) 
    return child

def compare_elements(a, b, attributes_to_exclude=None):
    '''
    Compare two elements for matching text, attributes, tails, tags and
    children.

    Args:
        a: First etree element to compare
        b: Second etree element to compare
        attributes_to_exclude: List of attributes to ignore in both
            elements
    Returns: True or false based on whether elements match
    
    '''
    if attributes_to_exclude is None:
        attributes_to_exclude = []
    elif not isinstance(attributes_to_exclude, list):
        attributes_to_exclude = [attributes_to_exclude]
    # TODO: remove copies
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
    # Run recursively to make sure children match as well
    equivalent_children = []
    for a_child in a.iterchildren():
        for b_child in b.iterchildren():
            if (b_child not in equivalent_children and
                compare_elements(a_child, b_child, attributes_to_exclude)):
                equivalent_children.append(b_child)
                break
    if len(equivalent_children) != len(list(a_copy)):
        return False
    return True


