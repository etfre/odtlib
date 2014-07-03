from lxml import etree
import tempfile
import zipfile
import os
from odtlib.utilities import shared, odt
from odtlib import style
from odtlib.namespace import NSMAP, qn

class BaseOdt:
    def __init__(self, filename):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '..', 'templates', 'new.odt')
        self._write_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, 'r') as odtzip:
            odtzip.extractall(self._write_dir)
        self._xmlfiles = shared.load_xml_files(self._write_dir)
        self._default_paragraph_style_name = shared.get_default_paragraph_style_name(self._xmlfiles['content.xml'])
        self._body = self._xmlfiles['content.xml'].find(qn('office', 'body'))
        self._text = self._body.find(qn('office', 'text'))
        odt.convert_to_spans(self._text)

    @property
    def _styles(self):
        '''
        Return a list of style wrappers.
        '''
        stylelist = []
        for styles in self._xmlfiles['content.xml'].iterchildren():
            if styles.tag in [qn('office', 'automatic-styles'), qn('office', 'styles')]:
                # xml parsing is never pretty
                for s in styles.iterchildren(qn('style', 'style')):
                    for k, v in s.attrib.items():
                        prefix = shared.get_prefix(k)
                        tag = shared.get_tag(k)
                        if tag == 'name': name = v
                        if tag == 'family': family = v
                    attribs = s.find(qn('style', 'text-properties')).attrib
                    stylelist.append(style.Style(s, name, family, attribs))
        return stylelist