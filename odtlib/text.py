import re
from odtlib.utilities import shared, textutilities
from odtlib.base import basetext
from odtlib import baselist
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
        super().__init__('p', style)
        data = set_data(text, style)
        self.spans = baselist.ElementList(self._ele, check_span_input, data=data)

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
        assert ele.tag == qn('text:p')
        para = cls(shared.get_paragraph_text(ele))
        para._ele = ele
        data = [Span._from_element(s) for s in ele.findall(qn('text:span'))]
        para.spans = baselist.ElementList(ele, check_span_input, data=data)
        return para

class Span(basetext.BaseText):
    def __init__(self, text='', style=None):
        super().__init__('span', style)
        self.text = text

    @classmethod
    def _from_element(cls, ele):
        span = cls(ele.text)
        span._ele = ele
        return span

class Heading(basetext.BaseText):
    '''
    Heading wrapper for <text: h> element.
    
    Attributes:
        spans: List of span wrappers representing the <text:span>
            elements that lie within this paragraph.
        text: String containing the entirety of the paragraph's text.
    '''

    def __init__(self, text='', style=None, level='1'):
        '''
        Constructor method for the Paragraph wrapper.

        Args:
            text: String that contains 
        '''
        super().__init__('h', style)
        self._style_copy.set(qn('style:parent-style-name'), 'Heading_20_{}'.format(level))
        self.level = level
        self._ele.set(qn('text:outline-level'), level)
        data = set_data(text, style)
        self.spans = baselist.ElementList(self._ele, check_span_input, data=data)

    @classmethod
    def _from_element(cls, ele):
        '''
        Create a heading wrapper for a <text:h> element. Used
        internally. Do **not** call this method as part of the odtlib
        API.

        Args:
            ele: etree <text:h> element off of which the
                wrapper is based
        Returns:
            Paragraph wrapper for <text:h> element
        '''
        assert ele.tag == qn('text:h')
        para = cls(shared.get_paragraph_text(ele))
        para._ele = ele
        data = [Span._from_element(s) for s in ele.findall(qn('text:span'))]
        para.spans = baselist.ElementList(ele, check_span_input, data=data)
        return para

def set_data(text, style):
    if text:
        return [Span(text)]
    return []

def check_paragraph_input(para):
    if isinstance(para, str):
        return Paragraph(para)
    if not isinstance(para, (Paragraph, Heading)):
        raise ValueError('Input to the paragraph list must be strings or Paragraph objects')
    return para

def check_span_input(span):
    if isinstance(span, str):
        return Span(span)
    if not isinstance(span, Span):
        raise ValueError('Input to the span list must be strings or Span objects')
    return span