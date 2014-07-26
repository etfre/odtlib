from lxml import etree
from odtlib.namespace import NSMAP, qn

FONT_WEIGHT = qn('fo:font-weight')
FONT_WEIGHT_ASIAN = qn('style:font-weight-asian')
FONT_WEIGHT_COMPLEX = qn('style:font-weight-complex')

FONT_STYLE = qn('fo:font-style')
FONT_STYLE_ASIAN = qn('style:font-style-asian')
FONT_STYLE_COMPLEX = qn('style:font-style-complex')

FONT_COLOR = qn('fo:color')

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

STANDARD_STYLES = {
	'Standard': '''<style:style xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
		style:class="text" style:family="paragraph" style:name="Standard"/>''',
	'Heading': '''<style:style xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
		xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" style:class="text"
		style:family="paragraph" style:name="Heading" style:next-style-name="Text_20_body"
		style:parent-style-name="Standard">
 			<style:paragraph-properties fo:keep-with-next="always" fo:margin-bottom="0.0835in"
 			fo:margin-top="0.1665in" style:contextual-spacing="false"/>
 			<style:text-properties fo:font-family="'Liberation Sans'" fo:font-size="14pt"
 			style:font-family-asian="'Droid Sans Fallback'" style:font-family-complex="FreeSans"
 			style:font-family-generic="swiss" style:font-family-generic-asian="system"
 			style:font-family-generic-complex="system" style:font-name="Liberation Sans"
 			style:font-name-asian="Droid Sans Fallback" style:font-name-complex="FreeSans"
 			style:font-pitch="variable" style:font-pitch-asian="variable"
 			style:font-pitch-complex="variable" style:font-size-asian="14pt" style:font-size-complex="14pt"/>
		</style:style>''',
	'Text_20_body': '''<style:style xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
		xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
		style:class="text" style:display-name="Text body" style:family="paragraph"
		style:name="Text_20_body" style:parent-style-name="Standard">
			<style:paragraph-properties fo:line-height="120%" fo:margin-bottom="0.0972in"
			fo:margin-top="0in" style:contextual-spacing="false"/>
		</style:style>''',
}


# <style:style style:class="list" style:family="paragraph" style:name="List" style:parent-style-name="Text_20_body">
# 	<style:text-properties style:font-family-complex="FreeSans" style:font-family-generic-complex="swiss" style:font-name-complex="FreeSans1" style:font-size-asian="12pt"/>
# </style:style>
# <style:style style:class="extra" style:family="paragraph" style:name="Caption" style:parent-style-name="Standard">
# 	<style:paragraph-properties fo:margin-bottom="0.0835in" fo:margin-top="0.0835in" style:contextual-spacing="false" text:line-number="0" text:number-lines="false"/>
# 	<style:text-properties fo:font-size="12pt" fo:font-style="italic" style:font-family-complex="FreeSans" style:font-family-generic-complex="swiss" style:font-name-complex="FreeSans1" style:font-size-asian="12pt" style:font-size-complex="12pt" style:font-style-asian="italic" style:font-style-complex="italic"/>
# </style:style>
# <style:style style:class="index" style:family="paragraph" style:name="Index" style:parent-style-name="Standard">
# 	<style:paragraph-properties text:line-number="0" text:number-lines="false"/>
# 	<style:text-properties style:font-family-complex="FreeSans" style:font-family-generic-complex="swiss" style:font-name-complex="FreeSans1" style:font-size-asian="12pt"/>
# </style:style>
# <style:style style:class="extra" style:family="paragraph" style:name="Header" style:parent-style-name="Standard">
# 	<style:paragraph-properties text:line-number="0" text:number-lines="false">
# 		<style:tab-stops>
# 			<style:tab-stop style:position="3.4626in" style:type="center"/>
# 			<style:tab-stop style:position="6.9252in" style:type="right"/>
# 		</style:tab-stops>
# 	</style:paragraph-properties>
# </style:style>