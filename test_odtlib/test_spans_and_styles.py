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
from odtlib import api

class TestSpansAndStyles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doc = api.OpenDocumentText(os.path.join(os.path.dirname(__file__), 'files', 'spansandstyles.odt'))

    def test_span_list_setup(self):
        for p in self.doc.paragraphs:
            for s in p.spans:
                self.assertIsInstance(s, text.Span)

    def test_span_list_length(self):
         self.assertEqual(len(self.doc.paragraphs[0].spans), 5)

    def test_span_list_setitem(self):
        self.doc.paragraphs[0].spans[0] = "Hello thar"
        self.doc.paragraphs[0].spans[-2] = "Lovely day we're having"
        self.assertEqual('Hello thar', self.doc.paragraphs[0].spans[0].text)
        self.assertEqual("Lovely day we're having", self.doc.paragraphs[0].spans[-2].text)
        self.doc.paragraphs[0].spans[0] = 'First span content.'
        self.doc.paragraphs[0].spans[-2] = 'Third span content.'

    def test_span_list_getitem(self):
        self.assertEqual('Second span content.', self.doc.paragraphs[0].spans[1].text)
        self.assertEqual("Third span content.", self.doc.paragraphs[0].spans[-3].text)

    def test_span_list_delete_and_insert(self):
        del self.doc.paragraphs[0].spans[0]
        self.assertEqual('Second span content.', self.doc.paragraphs[0].spans[0].text)
        self.doc.paragraphs[0].spans.insert(0, 'First span content.')
        self.assertEqual('First span content.', self.doc.paragraphs[0].spans[0].text)
        del self.doc.paragraphs[0].spans[-2]
        self.assertEqual('Third span content.', self.doc.paragraphs[0].spans[-2].text)
        self.doc.paragraphs[0].spans.insert(-2, 'Fourth span content.')
        self.assertEqual('Fourth span content.', self.doc.paragraphs[0].spans[-2].text)

    def test_span_list_append(self):
        self.doc.paragraphs[0].spans.append("I like avocados.")
        s = text.Span('They are delicious.')
        self.doc.paragraphs[0].spans.append(s)
        self.assertEqual('I like avocados.', self.doc.paragraphs[0].spans[-2].text)
        self.assertEqual('They are delicious.', self.doc.paragraphs[0].spans[-1].text)
        del self.doc.paragraphs[0].spans[-1]
        del self.doc.paragraphs[0].spans[-1]

    def test_span_list_extend(self):
        self.doc.paragraphs[0].spans.extend(['Second to last span', 'Last span!'])
        self.assertEqual('Second to last span', self.doc.paragraphs[0].spans[-2].text)
        self.assertEqual('Last span!', self.doc.paragraphs[0].spans[-1].text)
        del self.doc.paragraphs[0].spans[-1]
        del self.doc.paragraphs[0].spans[-1]

    def test_span_list_pop(self):
        p = self.doc.paragraphs[0].spans.pop()
        self.assertEqual('Fifth span content.', p.text)
        self.doc.paragraphs[0].spans.append(p)
        p = self.doc.paragraphs[0].spans.pop(1)
        self.assertEqual('Second span content.', p.text)
        self.doc.paragraphs[0].spans.insert(1, p)

        
    @classmethod
    def tearDownClass(cls):
        savename = 'spansandstylessave.odt'
        cls.doc.save(savename)
        cls.assertTrue(cls, os.path.isfile(savename))
        cls.assertTrue(cls, zipfile.is_zipfile(savename))
        os.remove(savename)

        

if __name__ == '__main__':
    unittest.main()