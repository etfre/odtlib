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

class TestParagraphs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.full_doc = api.Odt(os.path.join(os.path.dirname(__file__), 'files', 'paragraphs.odt'))

    def test_paragraph_list_setup(self):
        for p in self.full_doc.paragraphs:
            self.assertIsInstance(p, text.Paragraph)

    # def test_paragraph_list_setitem(self):
    #     self.full_doc.paragraphs[0] = "Hello thar"
    #     self.full_doc.paragraphs[-2] = "Lovely day we're having"
    #     self.assertEqual('Hello thar', self.full_doc.paragraphs[0].text)
    #     self.assertEqual("Lovely day we're having", self.full_doc.paragraphs[-2].text)
    #     self.full_doc.paragraphs[0] = 'First Placeholder Paragraph'
    #     self.full_doc.paragraphs[-2] = 'Fourth Placeholder Paragraph'

    # def test_paragraph_list_getitem(self):
    #     self.assertEqual('Second Placeholder Paragraph', self.full_doc.paragraphs[1].text)
    #     self.assertEqual("Third Placeholder Paragraph", self.full_doc.paragraphs[-3].text)

    def test_paragraph_list_delete_and_insert(self):
        del self.full_doc.paragraphs[0]
        self.assertEqual('Second Placeholder Paragraph', self.full_doc.paragraphs[0].text)
        self.full_doc.paragraphs.insert(0, 'First Placeholder Paragraph')
        self.assertEqual('First Placeholder Paragraph', self.full_doc.paragraphs[0].text)
        del self.full_doc.paragraphs[-2]
        self.assertEqual('Third Placeholder Paragraph', self.full_doc.paragraphs[-2].text)
        self.full_doc.paragraphs.insert(-2, 'Fourth Placeholder Paragraph')
        self.assertEqual('Fourth Placeholder Paragraph', self.full_doc.paragraphs[-2].text)

    def test_save(self):
        savename = 'paragraphssave.odt'
        self.full_doc.save(savename)
        self.assertTrue(os.path.isfile(savename))
        self.assertTrue(zipfile.is_zipfile(savename))
        # os.remove(savename)
        
    @classmethod
    def tearDownClass(cls):
        pass

        

if __name__ == '__main__':
    unittest.main()