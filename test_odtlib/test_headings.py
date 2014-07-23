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
        h = text.Heading('Hello world!', level='9')
        self.doc.paragraphs.append(h)

    @classmethod
    def tearDownClass(cls):
        savename = 'headingssave.odt'
        cls.doc.save(savename)
        cls.assertTrue(cls, os.path.isfile(savename))
        cls.assertTrue(cls, zipfile.is_zipfile(savename))
        # os.remove(savename)

        

if __name__ == '__main__':
    unittest.main()