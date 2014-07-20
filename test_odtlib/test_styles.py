import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from odtlib import text
from test_odtlib import specs
from odtlib import style
from odtlib import api
from odtlib.text import Paragraph

class TestStyles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doc = api.OpenDocumentText(os.path.join(os.path.dirname(__file__), 'files', 'styles.odt'))

    def test_text_property_getter1(self):
        p = self.doc.paragraphs[0]
        self.assertTrue(p.bold)
        self.assertEqual(p.color, '#6666ff')

    def test_default_style(self):
        s = style.Style('style name', 'paragraph')
        self.assertEqual(s.bold, None)
        self.assertEqual(s.italic, None)
        self.assertEqual(s.color, None)

    @classmethod
    def tearDownClass(cls):
        para_style1 = style.Style('para-style1', 'paragraph')
        para_style1.bold = True
        para_style1.color = '#b97531'
        span_style1 = style.Style('span-style1', 'text')
        span_style1.bold = False
        span_style1.color = '#56789a'
        p = Paragraph()
        p.spans.extend(['First span', 'Second span', 'Third span'])
        p.spans[0].style = span_style1
        p.spans[1].color = '#a98765'
        p.spans[1].bold = None
        p.spans[2].style = span_style1
        cls.doc.paragraphs.append(p)
        cls.doc.paragraphs.extend(['Fourth to last paragraph', 'Third to last paragraph',
                                   'Second to last paragraph', 'Last paragraph'])
        cls.doc.paragraphs[-4].style = para_style1
        cls.doc.paragraphs[-1].style = para_style1
        cls.doc.paragraphs[-3].color = '#ff1493'
        savename = 'stylessave.odt'
        cls.doc.save(savename)
        cls.testdoc = api.OpenDocumentText(savename)
        assert cls.testdoc.paragraphs[-4].bold == True
        assert cls.testdoc.paragraphs[-4].color == '#b97531'
        assert cls.testdoc.paragraphs[-3].color == '#ff1493'
        assert cls.testdoc.paragraphs[-2].color == None
        assert cls.testdoc.paragraphs[-1].bold == True
        assert cls.testdoc.paragraphs[-1].color == '#b97531'
        assert cls.testdoc.paragraphs[1].spans[0].color == '#56789a'
        assert cls.testdoc.paragraphs[1].spans[0].bold == False
        assert cls.testdoc.paragraphs[1].spans[1].color == '#a98765'
        assert cls.testdoc.paragraphs[1].spans[1].bold == None
        assert cls.testdoc.paragraphs[1].spans[2].color == '#56789a'
        assert cls.testdoc.paragraphs[1].spans[2].bold == False
        cls.testdoc.save('testdoc.odt')
        os.remove(savename)
        os.remove('testdoc.odt')

def get_and_set_testing():
    pass

if __name__ == '__main__':
    unittest.main()