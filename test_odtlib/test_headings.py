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

class TestHeadings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doc = api.OpenDocumentText(os.path.join(os.path.dirname(__file__), 'files', 'headings.odt'))

    def test_read_heading(self):
        self.assertIsInstance(self.doc.paragraphs[0], text.Heading)

    def test_heading_append(self):
        h = text.Heading()
        self.doc.paragraphs.append(h)
        self.assertEqual(self.doc.paragraphs[-1], h)
        del self.doc.paragraphs[-1]

    def test_heading_insert(self):
        h = text.Heading()
        self.doc.paragraphs.insert(-2, h)
        self.assertEqual(self.doc.paragraphs[-2], h)
        del self.doc.paragraphs[-2]

    def test_heading_constructor(self):
        h = text.Heading("Hello world!", level='3')
        self.assertEqual(h.text, "Hello world!")
        self.assertEqual(h.level, "3")

    def test_heading_text_setter_and_getter(self):
        h = text.Heading()
        h.text = 'Hello world!'
        self.assertEqual(h.text, 'Hello world!')

    def test_heading_text_change(self):
        h = text.Heading("Hello world!")
        h.text = "Goodbye world"
        self.assertEqual(h.text, "Goodbye world")

    @classmethod
    def tearDownClass(cls):
        savename = 'headingssave.odt'
        cls.doc.save(savename)
        cls.assertTrue(cls, os.path.isfile(savename))
        cls.assertTrue(cls, zipfile.is_zipfile(savename))
        os.remove(savename)

        

if __name__ == '__main__':
    unittest.main()