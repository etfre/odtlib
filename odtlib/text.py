import re
from odtlib import utilities
from odtlib.namespace import NSMAP, qn

class Paragraph:
    def __init__(self, ele=None, text=''):
        assert not (ele is not None and len(text))
        if ele is not None:
            self._ele = ele
        else:
            self._ele = utilities.makeelement('text', 'p', text)
        self.span_list = self.__build_span_list__()

    def search(self, value):
        '''
        Search the paragraph for a regular expression.
        '''
        match = re.search(value, self.text)
        if match is not None:
            return True
        return False

    def replace(self, search_value, replace_value):
        '''
        Replace all instances of a regular expression match in the paragraph with
        another string. If a match does not lie entirely within a single element,
        then the new text will be appended only to the first element in the match. 
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
        textlist = []
        if self._ele.text is not None:
            textlist.append(self._ele.text)
        for span in self._ele.iter(qn('text', 'span')):
            if span.text is not None:
                textlist.append(span.text)
            if span.tail is not None:
                textlist.append(span.tail)
        return ''.join(textlist)

    @text.setter
    def text(self, value):
        # If the new text value is shorter or different than before
        if len(value) < len(self.text) or value[:len(self.text)] != self.text:
            if self._ele.text is None and len(self.span_list):
                for i, child in enumerate(self._ele.iterchildren()):
                    if i == 0:
                        child.text = value
                        child.tail = None
                        continue
                    self._ele.remove(child)
                self.span_list = self.span_list[:1]
            else:
                utilities.remove_children(self._ele)
                self._ele.text = value
                self.span_list = []
        else:
            extra = value[len(self.text):]
            if len(self.span_list):
                if self.span_list[-1]._ele.tail is not None:
                    self.span_list[-1]._ele.tail = ''.join([ self.span_list[-1]._ele.tail, extra])
                else:
                    self.span_list[-1].text = ''.join([self.span_list[-1].text, extra])
            else:
                self._ele.text = value

    def __build_span_list__(self):
        span_list = []
        for etree_span in self._ele.iter(qn('text', 'span')):
            span = Span(ele=etree_span)
            span_list.append(span)
        return span_list

class Span:
    def __init__(self, ele=None, text=''):
        assert not (ele is not None and len(text))
        if ele is not None:
            self._ele = ele
        else:
            self._ele = utilities.makeelement('text', 'span', text)

    @property
    def text(self):
        return self._ele.text

    @text.setter
    def text(self, value):
        self._ele.text = value
