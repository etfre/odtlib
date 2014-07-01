import re
from odtlib import utilities
from odtlib.namespace import NSMAP, qn

class Paragraph:
    def __init__(self, ele=None, text=''):
        if ele is not None:
            self._ele = ele
        else:
            self._ele = utilities.makeelement('text', 'p', text)
        self._rawtext = ''
        if self._ele.text is not None:
            self._rawtext = self._ele.text
        self.span_list = self.__build_span_list__()
        for span in self.span_list:
            if span.text is not None:
                self._rawtext += span.text

    def search(self, value):
        '''
        Search the paragraph for a regular expression.
        '''
        match = re.search(value, self._rawtext)
        if match is not None:
            return True
        return False

    def replace(self, search_value, replace_value):
        '''
        Replace all instances of a regular expression match in the paragraph with
        another string. If a match does not lie entirely within a single element,
        then the new text will be appended only to the first element. 
        '''
        searchre = re.compile(search_value)
        match_slices = [match.span() for match in re.finditer(searchre, self.text)]
        eledict = utilities.create_replace_dict(self._ele, match_slices)
        # replace in reversed order to avoid dealing with shifted index positions
        for match in reversed(match_slices):
            for ele, info in reversed(list(eledict.items())):
                if info[0] <= match[1]:
                    if match[0] < info[0]:
                         ele.text = utilities.remove_substr(0, match[1] - info[0], ele.text)
                    else:
                        ele.text = utilities.remove_substr(match[0] - info[0], match[1] - info[0], ele.text)
                        ele.text = utilities.insert_substr(match[0] - info[0], replace_value, ele.text)
                        break              
        utilities.merge_placeholders(eledict)
#         
    @property
    def text(self):
        testlist = []
        if self._ele.text is not None:
            testlist.append(self._ele.text)
        for span in self._ele.iter(qn('text', 'span')):
            if span.text is not None:
                testlist.append(span.text)
            if span.tail is not None:
                testlist.append(span.tail)
        return ''.join(testlist)

    @text.setter
    def text(self, value):
        #FIXME
        if len(value) < len(self._rawtext) or value[:len(self._rawtext)] != self._rawtext:
            utilities.remove_children(self._ele)
            self._ele.text = value
            self.span_list = []
        else:
            extra = value[len(self._rawtext):]
            if len(self.span_list):
                self.span_list[-1].text += extra
            else:
                self._ele.text = value
        self._rawtext = value

    def __build_span_list__(self):
        span_list = []
        for etree_span in self._ele.iter(qn('text', 'span')):
            span = Span(ele=etree_span)
            span_list.append(span)
        return span_list

class Span:
    def __init__(self, ele=None, text=''):
        if ele is not None:
            self._ele = ele
        else:
            self._ele = utilities.makeelement('text', 'span', text)
        self._rawtext = self._ele.text

    @property
    def text(self):
        return self._rawtext

    @text.setter
    def text(self, value):
        self._rawtext = value
        self._ele.text = value