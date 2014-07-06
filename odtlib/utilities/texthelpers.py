from odtlib.namespace import NSMAP, qn

def update_spans(pwrapper):
	pwrapper.spans._list = []
	pwrapper.spans.extend([Span._from_element(s) for s in pwrapper._ele.findall(qn('text', 'span'))])

