from odtlib.namespace import NSMAP, qn
from odtlib.utilities import shared

def attach_style_wrapper(text_wrapper, styles):
	stylename = shared.get_style_name(text_wrapper._ele)
	try:
		text_wrapper.style = styles[stylename]
	except KeyError:
		text_wrapper.style = None
	if text_wrapper._ele.tag == qn('text:p'):
		for span in text_wrapper.spans:
			attach_style_wrapper(span, styles)