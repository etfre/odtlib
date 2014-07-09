from odtlib.namespace import qn

BASE_STYLE_PROPERTIES = {
	'bold': False,
	'italics': False
}

FONT_WEIGHT = qn('fo', 'font-weight')
FONT_WEIGHT_ASIAN = qn('style', 'font-weight-asian')
FONT_WEIGHT_COMPLEX = qn('style', 'font-weight-complex')

FONT_STYLE = qn('fo', 'font-style')
FONT_STYLE_ASIAN = qn('style', 'font-style-asian')
FONT_STYLE_COMPLEX = qn('style', 'font-style-complex')

STYLE_ATTRIBUTES = {
	'bold': (FONT_WEIGHT, FONT_WEIGHT_ASIAN, FONT_WEIGHT_COMPLEX),
	'italic': (FONT_STYLE, FONT_STYLE_ASIAN, FONT_STYLE_COMPLEX)
}