from lxml import etree
import tempfile
import zipfile
import os
from odtlib.utilities import shared, odt
from odtlib import style
from odtlib.namespace import NSMAP, qn

class BaseOpenDocumentText:
    def __init__(self, filename):
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '..', 'templates', 'new.odt')
        self._write_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, 'r') as odtzip:
            odtzip.extractall(self._write_dir)
        self._xmlfiles = shared.load_xml_files(self._write_dir)
        self._content = self._xmlfiles['content.xml']
        self._automatic_styles, self._office_styles = odt.get_style_containers(self._content)
        self._body = self._xmlfiles['content.xml'].find(qn('office', 'body'))
        self._text = self._body.find(qn('office', 'text'))
        self._default_styles = odt.get_default_styles(self._xmlfiles['styles.xml'])
        odt.convert_to_spans(self._text)

    def _update_styles(self):
        pass
        # for para in self.paragraphs:
        #     para_style = para._get_or_build_style(self.styles)
            # style.update_style(para, self._automatic_styles, self._office_styles)
            # for span in para.spans:
            #     style.update_style(span, self._automatic_styles, self._office_styles)

    def __enter__(self):
        pass

    def __exit__ (self, type, value, tb):
        pass

