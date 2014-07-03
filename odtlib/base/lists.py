from collections import MutableSequence
from odtlib import utilities
from odtlib.text import Paragraph, Span
from odtlib.namespace import NSMAP, qn

class ParagraphList:
    def __init__(self, parent, default_style, data=[]):
        super().__init__()
        self._parent = parent
        self._default_style = default_style
        self._list = []
        self._list.extend(data)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __delitem__(self, i):
        self._parent.remove(self._list[i]._ele)
        del self._list[i]

    def __setitem__(self, i, para):
        para = check_paragraph_input(para, self._default_style)
        new_i = self._parent.index(self._list[i]._ele)
        self._parent.remove(self._list[i]._ele)
        self._parent.insert(new_i, para._ele)
        self._list[i] = para

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{}'.format(self._list)

    def append(self, para):
        para = check_paragraph_input(para, self._default_style)
        self._list.append(para)
        self._parent.append(para._ele)

    def extend(self, paralist):
        for para in paralist:
            para = check_paragraph_input(para, self._default_style)
            self._list.append(para)
            self._parent.append(para._ele)            

    def insert(self, i, para):
        para = check_paragraph_input(para, self._default_style)
        i = reverse_index(i, self._list)
        shift = get_shift(i, self._parent)
        self._parent.insert(i+shift, para._ele)
        self._list.insert(i, para)

    def pop(self, i=-1):
        self._parent.remove(self._list[i]._ele)
        return self._list.pop(i)

    def remove(self, para):
        check_paragraph_input(para, self._default_style)
        if isinstance(para, str):
            for pwrapper in self._list:
                if pwrapper.text == para:
                    self._parent.remove(pwrapper._ele)
                    self._list.remove(pwrapper)
                    return
            raise ValueError('list.remove(x): x not in list')
        else:
            self._list.remove(para)
            self._parent.remove(para._ele)

def check_paragraph_input(para, style):
    if isinstance(para, str):
        return Paragraph(para, style=style)
    if not isinstance(para, Paragraph):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para

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