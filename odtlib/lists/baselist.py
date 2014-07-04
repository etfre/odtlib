from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn

class ElementList:
    def __init__(self, parent, check_function, default_style=None, data=[]):
        '''
        Container for Paragraph and Span wrappers.
        '''
        # print(data)
        self._parent = parent
        self._check_function = check_function
        self._default_style = default_style
        self._list = []
        self._list.extend(data)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{}'.format(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __delitem__(self, i):
        self._parent.remove(self._list[i]._ele)
        del self._list[i]

    def __setitem__(self, i, wrapper):
        wrapper = self._check_function(wrapper, self._default_style)
        new_i = self._parent.index(self._list[i]._ele)
        self._parent.remove(self._list[i]._ele)
        self._parent.insert(new_i, wrapper._ele)
        self._list[i] = wrapper

    def append(self, wrapper):
        wrapper = self._check_function(wrapper, self._default_style)
        self._list.append(wrapper)
        self._parent.append(wrapper._ele)

    def extend(self, wrapperlist):
        for wrapper in wrapperlist:
            wrapper = self._check_function(wrapper, self._default_style)
            self._list.append(wrapper)
            self._parent.append(wrapper._ele)

    def insert(self, i, wrapper):
        wrapper = self._check_function(wrapper, self._default_style)
        i = reverse_index(i, self._list)
        shift = get_shift(i, self._parent)
        self._parent.insert(i+shift, wrapper._ele)
        self._list.insert(i, wrapper)   

    def pop(self, i=-1):
        self._parent.remove(self._list[i]._ele)
        return self._list.pop(i)

    def remove(self, wrapper):
        self._check_function(wrapper, self._default_style)
        if isinstance(wrapper, str):
            for pwrapper in self._list:
                if pwrapper.text == wrapper:
                    self._parent.remove(pwrapper._ele)
                    self._list.remove(pwrapper)
                    return
            raise ValueError('list.remove(x): x not in list')
        else:
            self._list.remove(wrapper)
            self._parent.remove(wrapper._ele)

def check_paragraph_input(para, style):
    if isinstance(para, str):
        return text.Paragraph(para, style)
    if not isinstance(para, text.Paragraph):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para

def check_span_input(span, style):
    if isinstance(span, str):
        return text.Span(span, style)
    if not isinstance(span, text.Span):
        raise ValueError('Input to the span list must be strings or Span objects')
    return span

def check_style_input(style, default):
    assert default is None
    if not isinstance(span, text.Style):
        raise ValueError('Input to the style list must be Style objects')

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
    For every child that is a wrappergraph, increment shift by one.
    We do this to account for non-wrappergraph children of <office:text>
    while we are doing indexing operations
    '''
    shift = 0
    for index, child in enumerate(ele.iterchildren()):
        if child.tag != qn('text', 'p'):
            shift += 1
        if index > i:
            break
    return shift