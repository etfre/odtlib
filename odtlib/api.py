from lxml import etree
import os
import shutil
import re
from odtlib import text, style
from odtlib.lists import baselist
from odtlib.base import baseodt
from odtlib.utilities import shared, odt
from odtlib.namespace import NSMAP, qn

class Odt(baseodt.BaseOdt):
    def __init__(self, filename=None):
        super().__init__(filename)
        data = [text.Paragraph._from_element(p) for p in self._text.findall(qn('text', 'p'))]
        self.paragraphs = baselist.ElementList(self._text,
                                               text.check_paragraph_input,
                                               self._default_paragraph_style_name,
                                               data=data)
        # self.styles = style.build_styles_list(self._xmlfiles['content.xml'])

    def save(self, filename):
        odt.convert_from_spans(self._text)
        # style.update_styles(self._xmlfiles['content.xml'], self.styles)
        shared.write_xml_files(self._xmlfiles, self._write_dir)
        shutil.make_archive(filename, 'zip', self._write_dir)
        os.rename('{}.zip'.format(filename), filename),
        shutil.rmtree(self._write_dir)
        assert len(self.paragraphs) == len(self._text.findall(qn('text', 'p')))

    def search(self, value):
        return [para for para in self.paragraphs if para.search(value)]

    def replace(self, search_value, replace_value):
        for para in self.paragraphs:
            para.replace(search_value, replace_value)