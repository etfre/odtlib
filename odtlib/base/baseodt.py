from lxml import etree
import tempfile
import zipfile
import os
from odtlib.utilities import shared, odt, styleutilities
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
        self._styles_elements = odt.get_style_containers(self._xmlfiles['content.xml'], self._xmlfiles['styles.xml'])
        styleutilities.update_styles_file(self._styles_elements['stylefile office'])
        self._text = self._xmlfiles['content.xml'].find(qn('office:body')).find(qn('office:text'))
        self._default_styles = odt.get_default_styles(self._xmlfiles['styles.xml'])
        odt.convert_to_spans(self._text)

    def _update_styles(self):
        for para in self.paragraphs:
            para._attach_style(self._styles_elements)
            for span in para.spans:
                span._attach_style(self._styles_elements)

    def __enter__(self):
        doc = self.__init__()

    def __exit__ (self, type, value, tb):
        pass

