from odtlib.namespace import qn

BASE_STYLE_PROPERTIES = {
	'bold': None,
	'italics': None,
	'color': None,
}

FONT_WEIGHT = qn('fo', 'font-weight')
FONT_WEIGHT_ASIAN = qn('style', 'font-weight-asian')
FONT_WEIGHT_COMPLEX = qn('style', 'font-weight-complex')

FONT_STYLE = qn('fo', 'font-style')
FONT_STYLE_ASIAN = qn('style', 'font-style-asian')
FONT_STYLE_COMPLEX = qn('style', 'font-style-complex')

FONT_COLOR = qn('fo', 'color')

STYLE_ATTRIBUTES = {
	'bold': (FONT_WEIGHT, FONT_WEIGHT_ASIAN, FONT_WEIGHT_COMPLEX),
	'italic': (FONT_STYLE, FONT_STYLE_ASIAN, FONT_STYLE_COMPLEX),
	'color': [FONT_COLOR],
}

PROPERTY_INPUT_MAP = {
	'bold': {True: 'bold', False: 'normal'},
	'italic': {True: 'italic', False: 'normal'},
	'color': {},
}

COLOR_DICT = {
	'black': '#000000',
}