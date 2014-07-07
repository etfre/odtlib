import re
from odtlib.utilities import shared, texthelpers
from odtlib.base import basetext
from odtlib.lists import baselist
from odtlib.namespace import NSMAP, qn

class Paragraph(basetext.BaseText):
    def __init__(self, text='', style=None):
        super().__init__(style)
        self._ele = shared.makeelement('text', 'p')
        data = []
        if text:
            data.append(Span(text))
        self.spans = baselist.ElementList(self._ele, check_span_input, data=data)

    @classmethod
    def _from_element(cls, ele):
        para = cls()
        para.text = shared.get_paragraph_text(ele)
        para.style = shared.get_style_name(ele)
        para._ele = ele
        data = [Span._from_element(s) for s in ele.findall(qn('text', 'span'))]
        para.spans = baselist.ElementList(ele, check_span_input, data=data)
        return para

    def search(self, value):
        '''
        Search the paragraph for a regular expression match.
        '''
        match = re.search(value, self.text)
        if match is not None:
            return True
        return False

    def replace(self, search_value, replace_value):
        '''
        Replace all instances of a regular expression match in the paragraph with
        another string. If a match does not lie entirely within a single span,
        then the new text will be appended only to the first span in the match. 
        '''
        searchre = re.compile(search_value)
        match_slices = [match.span() for match in re.finditer(searchre, self.text)]
        eledict = shared.create_replace_dict(self, match_slices)
        # replace in reversed order to avoid dealing with shifted index positions
        for match in reversed(match_slices):
            for ele, info in reversed(list(eledict.items())):
                if info[0] <= match[1]:
                    if match[0] < info[0]:
                         ele.text = shared.remove_substr(0, match[1] - info[0], ele.text)
                    else:
                        ele.text = shared.remove_substr(match[0] - info[0], match[1] - info[0], ele.text)
                        ele.text = shared.insert_substr(match[0] - info[0], replace_value, ele.text)
                        break

    @property
    def text(self):
        from_wrappers = ''.join([span.text for span in self.spans])
        from_elements = shared.get_paragraph_text(self._ele)
        assert from_wrappers == from_elements
        return from_elements

    @text.setter
    def text(self, value):
        # If the new text value is shorter or different than before
        if len(value) < len(self.text) or value[:len(self.text)] != self.text:
            del self.spans[:]
            self.spans.append(value) 
        else:
            extra = value[len(self.text):]
            if self._ele.findall(qn('text', 'span')):
               self.spans[-1].text += extra
            else:
                self.spans.append(extra)

class Span(basetext.BaseText):
    def __init__(self, text='', style=None):
        super().__init__(style)
        self._ele = shared.makeelement('text', 'span', text)

    @classmethod
    def _from_element(cls, ele):
        span = cls(ele.text, shared.get_style_name(ele))
        span._ele = ele
        return span

    @property
    def text(self):
        return self._ele.text

    @text.setter
    def text(self, value):
        self._ele.text = value


def check_paragraph_input(para, style):
    if isinstance(para, str):
        return Paragraph(para, style)
    if not isinstance(para, Paragraph):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para

def check_span_input(span, style):
    if isinstance(span, str):
        return Span(span, style)
    if not isinstance(span, Span):
        raise ValueError('Input to the span list must be strings or Span objects')
    return span