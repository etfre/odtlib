from lxml import etree
import os
import shutil
import re
from odtlib import text, style
from odtlib import baselist
from odtlib.base import baseodt
from odtlib.utilities import shared, odt, textutilities
from odtlib.namespace import NSMAP, qn

class OpenDocumentText(baseodt.BaseOpenDocumentText):
    def __init__(self, filename=None):
        super().__init__(filename)
        data = []
        for ele in self._text:
            if ele.tag == qn('text:p'):
                data.append(text.Paragraph._from_element(ele))
            elif ele.tag == qn('text:h'):
                data.append(text.Heading._from_element(ele))
        self.paragraphs = baselist.ElementList(self._text,
                                               text.check_paragraph_input,
                                               data=data)
        self.styles = style.build_styles_dict(self._styles_elements)
        for paragraph in self.paragraphs:
            textutilities.attach_style_wrapper(paragraph, self.styles)

    def save(self, filename):
        self._update_styles()
        odt.convert_from_spans(self._text)
        shared.write_xml_files(self._xmlfiles, self._write_dir)
        shutil.make_archive(filename, 'zip', self._write_dir)
        os.rename('{}.zip'.format(filename), filename),
        shutil.rmtree(self._write_dir)
        assert len(self.paragraphs) == (len(self._text.findall(qn('text:p'))) +
            len(self._text.findall(qn('text:h'))))

    def search(self, value):
        return [para for para in self.paragraphs if para.search(value)]

    def replace(self, search_value, replace_value):
        for para in self.paragraphs:
            para.replace(search_value, replace_value)