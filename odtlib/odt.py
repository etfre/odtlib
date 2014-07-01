from lxml import etree
import os
import shutil
import re
from odtlib.text import Paragraph, Span
from odtlib.base.baseodt import BaseOdt
from odtlib import utilities
from odtlib.namespace import NSMAP, qn

class Odt(BaseOdt):
    def __init__(self, filename=None):
        super().__init__(filename)
        self.paragraph_list = self.__build_paragraph_list__()

    def save(self, filename):
        utilities.write_xml_files(self._xmlfiles, self._write_dir)
        shutil.make_archive(filename, 'zip', self._write_dir)
        os.rename('{}.zip'.format(filename), filename)
        shutil.rmtree(self._write_dir)
        assert len(self.paragraph_list) == len(self._text.findall(qn('text', 'p')))

    def add_paragraph(self, text='', pos=None):
        '''
        Add a paragraph to the document.
        '''
        if pos is None:
            pos = len(self.paragraph_list)
        ele = utilities.makeelement('text', 'p', text)
        if pos == 0:
            self._text.insert(0, ele)
        else:
            for i, etree_para in enumerate(self._text.iter(qn('text', 'p')), start=1):
                sibling = etree_para
                if i == pos: break
            sibling.addnext(ele)
        self.paragraph_list.insert(pos, Paragraph(ele))
        assert len(self.paragraph_list) == len(self._text.findall(qn('text', 'p')))
    
    def search(self, value):
        return [para for para in self.paragraph_list if para.search(value)]

    def replace(self, search_value, replace_value):
        for para in self.paragraph_list:
            para.replace(search_value, replace_value)