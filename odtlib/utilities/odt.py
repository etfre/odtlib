from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn
from odtlib import style

def convert_to_spans(text_parent):
    '''
    Convert all paragraph text to spans for easier API handling.
    This will be reversed when the document is saved.
    '''
    # for para in text_parent.iterchildren(qn('text', 'p')):
    # 	style_name = shared.get_style_name(para)
    # 	s = style.Style._from_element("ss")
    # 	print(s)
    pass