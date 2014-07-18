from odtlib.namespace import NSMAP, qn
from odtlib.utilities import shared

def set_property(wrapper, prop, value):
    if wrapper._style_properties[prop] != value:
        wrapper._style_properties[prop] = value
        wrapper.style = None
    if apply_to_spans and wrapper._ele.tag == qn('text', 'p'):
        for span in wrapper.spans:
            set_property(span, prop, value)


def assign_paragraph_properties(paragraph, styles):
	'''
	Find the <style: text-properties> element that corresponds to the
	given paragraph wrapper. Then, given the attributes of that text-properties
	element, set the properties (bold, italics etc.) of the paragraph wrapper and
	its span wrappers. Then, do the same with each span wrapper, overwriting
	wherever specified. This is because children inherit style properties of
	their parents, with the most immediate style parts taking precedence if parts of
	the styles contradict each other.
	'''
	pass

def attach_style_wrapper(text_wrapper, styles):
	stylename = shared.get_style_name(text_wrapper._ele)
	try:
		text_wrapper.style = styles[stylename]
	except KeyError:
		text_wrapper.style = None
	if text_wrapper._ele.tag == qn('text', 'p'):
		for span in text_wrapper.spans:
			attach_style_wrapper(span, styles)