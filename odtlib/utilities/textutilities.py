from odtlib.namespace import NSMAP, qn
from odtlib.utilities import shared

def attach_style_wrapper(text_wrapper, styles):
    '''
    Attach a style wrapper to the style field of a text wrapper. If a
    paragraph or a heading, do the same for all spans in the text
    wrapper

    Args:
        text_wrapper: Wrapper of a text element that is a child of
            <office:text>
        styles: Dict mapping style names to their corresponding
            wrappers
    '''
    stylename = shared.get_style_name(text_wrapper._ele)
    try:
        text_wrapper.style = styles[stylename]
    except KeyError:
        text_wrapper.style = None
    if text_wrapper._ele.tag in (qn('text:p'), qn('text:h')):
        for span in text_wrapper.spans:
            attach_style_wrapper(span, styles)

def get_paragraph_text(para):
    textlist = []
    if para.text is not None:
        textlist.append(para.text)
    for span in para.iter(qn('text:span')):
        if span.text is not None:
            textlist.append(span.text)
        if span.tail is not None:
            textlist.append(span.tail)
    if para.tail is not None:
        textlist.append(para.tail)
    return ''.join(textlist)

def parse_text(ele):
    textlist = []
    pos = 0
    print(ele.text)
    print(list(ele))

def append_to_last(ele, textlist):
    if textlist:
        if list(ele):
            list(ele)[-1].tail = ''.join(textlist)
        else:
            ele.text = ''.join(textlist)
