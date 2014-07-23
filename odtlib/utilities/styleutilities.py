from lxml import etree
from odtlib.namespace import NSMAP, qn
from odtlib import constants

def update_styles_file(ele):
	for name, elestring in constants.STANDARD_STYLES.items():
		if name not in [style.get(qn('style:name')) for style in list(ele)]:
			ele.append(etree.fromstring(elestring))