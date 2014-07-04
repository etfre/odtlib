from odtlib.lists import baselist
from odtlib import text
from odtlib.utilities import listhelpers
from odtlib.namespace import NSMAP, qn

class ParagraphList(baselist.ElementList):
    def __init__(self, parent, default_style, data=[]):
        super().__init__(parent, listhelpers.check_paragraph_input, default_style, data)         


def reverse_index(i, wrapper_list):
    '''
    Only used for the insert method
    '''

    if i < 0:
        i = len(wrapper_list) + i + 1
    return i

def get_shift(i, ele):
    '''
    Iterate over children of <office:text> element to position i.
    For every child that is a paragraph, increment shift by one.
    We do this to account for non-paragraph children of <office:text>
    while we are doing indexing operations
    '''
    shift = 0
    for index, child in enumerate(ele.iterchildren()):
        if child.tag != qn('text', 'p'):
            shift += 1
        if index > i:
            break
    return shift