from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn

class ElementList:
    def __init__(self, parent, check_function, data=None):
        '''
        Container for Paragraph/Heading and Span wrappers.
        '''
        self._parent = parent
        self._check_function = check_function
        self._list = []
        if data is not None:
            self._parent.extend([wrapper._ele for wrapper in data])
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
        if isinstance(i, slice):
            modlist = get_correct_children(self._parent)
            assert len(modlist) == len(self._list)
            start, stop, step = get_slice_info(i, modlist)
            if start < stop:
                start, stop = stop - 1, start - 1
                step = -step
            for pos in range(start, stop, step):
                self._parent.remove(modlist[pos])
                del self._list[pos]
        else:
            self._parent.remove(self._list[i]._ele)
            del self._list[i]

    def __setitem__(self, i, wrapper):
        wrapper = self._check_function(wrapper)
        self._parent.replace(self._list[i]._ele, wrapper._ele)
        self._list[i] = wrapper

    def append(self, wrapper):
        wrapper = self._check_function(wrapper)
        self._list.append(wrapper)
        self._parent.append(wrapper._ele)

    def extend(self, wrapperlist):
        for wrapper in wrapperlist:
            wrapper = self._check_function(wrapper)
            self._list.append(wrapper)
            self._parent.append(wrapper._ele)

    def insert(self, i, wrapper):
        wrapper = self._check_function(wrapper)
        i = reverse_index(i, self._list)
        shift = get_shift(i, self._parent)
        self._parent.insert(i+shift, wrapper._ele)
        self._list.insert(i, wrapper)

    def pop(self, i=-1):
        self._parent.remove(self._list[i]._ele)
        return self._list.pop(i)

    def remove(self, wrapper):
        self._check_function(wrapper)
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
        if child.tag not in (qn('text:p'), qn('text:h')):
            shift += 1
        if index > i:
            break
    return shift

def get_correct_children(parent):
    assert parent.tag in [qn('office:text'), qn('text:p'), qn('text:h')]
    if parent.tag == qn('office:text'):
        children = []
        for child in parent.iterchildren():
            if child.tag in (qn('text:p'), qn('text:h')):
                children.append(child)
        return children
    else:
        return parent.findall(qn('text:span'))

def get_slice_info(i, modlist):
    start = i.start
    if start is None: start = 0
    stop = i.stop
    if stop is None: stop = len(modlist)
    step = i.step
    if step is None: step = 1
    return start, stop, step