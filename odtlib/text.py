import re
from odtlib.utilities import shared, textutilities
from odtlib.base import basetext
from odtlib.lists import baselist
from odtlib.namespace import NSMAP, qn

class Paragraph(basetext.BaseText):
    '''
    Paragraph wrapper for <text: p> element. Note that all of the
    style-based properties of this class, such as bold or italic,
    can be set to None, in which case they will defer to the default
    document style for that property.

    Attributes:
        spans: List of span wrappers representing the <text: span>
            elements that lie within this paragraph.
        text: String containing the entirety of the paragraph's text.
        bold: Bool indicating whether or not this paragraph's text
            displays as bold.

    '''

    def __init__(self, text='', style=None):
        '''
        Constructor method for the Paragraph wrapper.

        Args:
            text: String that contains 
        '''
        self._ele = shared.makeelement('text', 'p')
        data = []
        if text:
            data.append(Span(text))
        self.spans = baselist.ElementList(self._ele, check_span_input, data=data)
        super().__init__(style)

    @classmethod
    def _from_element(cls, ele):
        '''
        Create a paragraph wrapper for a <text: p> element. Used
        internally. Do **not** call this method as part of the odtlib
        API.

        Args:
            ele: etree <text: p> element off of which the
                wrapper is based
        Returns:
            Paragraph wrapper for <text: p> element
        '''
        assert ele.tag == qn('text', 'p')
        para = cls(shared.get_paragraph_text(ele))
        para._ele = ele
        data = [Span._from_element(s) for s in ele.findall(qn('text', 'span'))]
        para.spans = baselist.ElementList(ele, check_span_input, data=data)
        return para

    def search(self, value):
        '''
        Search the paragraph text for a regular expression match.

        Args:
            search_value(str): Regex pattern to find in paragraph text
        Returns:
            A bool value depending on whether at least one match of the
            value pattern was found in the paragraph text
        '''
        if re.search(value, self.text) is not None:
            return True
        return False

    def replace(self, search_value, replace_value):
        '''
        Replace all instances of a regular expression match in the paragraph with
        another string. If a match does not lie entirely within a single span,
        then the new text will be appended only to the first span in the match.

        Args:
            search_value(str): String to find in paragraph text
            replace_value(str): New string that replaces all instances
                of search_value
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
        span = cls(ele.text)
        span._ele = ele
        return span

    @property
    def text(self):
        if self._ele.text is None:
            return ''
        return self._ele.text

    @text.setter
    def text(self, value):
        self._ele.text = value


def check_paragraph_input(para):
    if isinstance(para, str):
        return Paragraph(para)
    if not isinstance(para, Paragraph):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para

def check_span_input(span):
    if isinstance(span, str):
        return Span(span)
    if not isinstance(span, Span):
        raise ValueError('Input to the span list must be strings or Span objects')
    return span