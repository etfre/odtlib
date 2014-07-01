from lxml import etree
import tempfile
import zipfile
import os
import shutil
from odtlib import utilities
from odtlib.style import Style
from odtlib.namespace import NSMAP, qn
from odtlib.text import Paragraph, Span

class BaseOdt:
    def __init__(self, filename):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '..', 'templates', 'new.odt')
        self._write_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, 'r') as odtzip:
            odtzip.extractall(self._write_dir)
        self._xmlfiles = utilities.load_xml_files(self._write_dir)
        self._body = self._xmlfiles['content.xml'].find(qn('office', 'body'))
        self._text = self._body.find(qn('office', 'text'))

    def __build_paragraph_list__(self):
        para_list = []
        for etree_para in self._body.iter(qn('text', 'p')):
            p = Paragraph(ele=etree_para)
            para_list.append(p)
        return para_list

    @property
    def _styles(self):
        '''
        Return a list of style wrappers.
        '''
        stylelist = []
        for styles in self._xmlfiles['content.xml'].iterchildren():
            if styles.tag in [qn('office', 'automatic-styles'), qn('office', 'styles')]:
                # xml parsing is never pretty
                for style in styles.iterchildren(qn('style', 'style')):
                    for k, v in style.attrib.items():
                        prefix = utilities.get_prefix(k)
                        tag = utilities.get_tag(k)
                        if tag == 'name': name = v
                        if tag == 'family': family = v
                    attribs = style.find(qn('style', 'text-properties')).attrib
                    stylelist.append(Style(style, name, family, attribs))
        return stylelist