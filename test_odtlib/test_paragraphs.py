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
        cls.doc = api.OpenDocumentText(os.path.join(os.path.dirname(__file__), 'files', 'paragraphs.odt'))

    def test_paragraph_list_setup(self):
        for p in self.doc.paragraphs:
            self.assertIsInstance(p, text.Paragraph)

    def test_paragraph_list_length(self):
         self.assertEqual(len(self.doc.paragraphs), 5)

    def test_paragraph_list_setitem(self):
        self.doc.paragraphs[0] = "Hello thar"
        self.doc.paragraphs[-2] = "Lovely day we're having"
        self.assertEqual('Hello thar', self.doc.paragraphs[0].text)
        self.assertEqual("Lovely day we're having", self.doc.paragraphs[-2].text)
        self.doc.paragraphs[0] = 'First Placeholder Paragraph'
        self.doc.paragraphs[-2] = 'Fourth Placeholder Paragraph'

    def test_paragraph_list_getitem(self):
        self.assertEqual('Second Placeholder Paragraph', self.doc.paragraphs[1].text)
        self.assertEqual("Third Placeholder Paragraph", self.doc.paragraphs[-3].text)

    def test_paragraph_list_delete_and_insert(self):
        del self.doc.paragraphs[0]
        self.assertEqual('Second Placeholder Paragraph', self.doc.paragraphs[0].text)
        self.doc.paragraphs.insert(0, 'First Placeholder Paragraph')
        self.assertEqual('First Placeholder Paragraph', self.doc.paragraphs[0].text)
        del self.doc.paragraphs[-2]
        self.assertEqual('Third Placeholder Paragraph', self.doc.paragraphs[-2].text)
        self.doc.paragraphs.insert(-2, 'Fourth Placeholder Paragraph')
        self.assertEqual('Fourth Placeholder Paragraph', self.doc.paragraphs[-2].text)

    def test_paragraph_list_delete_slice(self):
        del self.doc.paragraphs[0:2]
        self.assertEqual('Third Placeholder Paragraph', self.doc.paragraphs[0].text)
        self.doc.paragraphs.insert(0, 'First Placeholder Paragraph')
        self.doc.paragraphs.insert(1, 'Second Placeholder Paragraph')
        del self.doc.paragraphs[4:-1:-2]
        self.assertEqual('Second Placeholder Paragraph', self.doc.paragraphs[0].text)
        self.assertEqual('Fourth Placeholder Paragraph', self.doc.paragraphs[1].text)
        self.assertEqual(len(self.doc.paragraphs), 2)
        self.doc.paragraphs.insert(0, 'First Placeholder Paragraph')
        self.doc.paragraphs.insert(2, 'Third Placeholder Paragraph')
        self.doc.paragraphs.insert(4, 'Fifth Placeholder Paragraph')

    def test_paragraph_list_append(self):
        self.doc.paragraphs.append("I like avocados.")
        p = text.Paragraph('They are delicious.')
        self.doc.paragraphs.append(p)
        self.assertEqual('I like avocados.', self.doc.paragraphs[-2].text)
        self.assertEqual('They are delicious.', self.doc.paragraphs[-1].text)
        del self.doc.paragraphs[-1]
        del self.doc.paragraphs[-1]

    def test_paragraph_list_extend(self):
        self.doc.paragraphs.extend(['Second to last paragraph', 'Last paragraph!'])
        self.assertEqual('Second to last paragraph', self.doc.paragraphs[-2].text)
        self.assertEqual('Last paragraph!', self.doc.paragraphs[-1].text)
        del self.doc.paragraphs[-1]
        del self.doc.paragraphs[-1]

    def test_paragraph_list_pop(self):
        p = self.doc.paragraphs.pop()
        self.assertEqual('Fifth Placeholder Paragraph', p.text)
        self.doc.paragraphs.append(p)
        p = self.doc.paragraphs.pop(1)
        self.assertEqual('Second Placeholder Paragraph', p.text)
        self.doc.paragraphs.insert(1, p)

    def test_paragraph_list_remove(self):
        self.doc.paragraphs.remove("Second Placeholder Paragraph")
        self.assertEqual('Third Placeholder Paragraph', self.doc.paragraphs[1].text)
        self.doc.paragraphs.insert(1, 'Second Placeholder Paragraph')
        missing_string = "Can't find me!"
        with self.assertRaises(ValueError):
            self.doc.paragraphs.remove(missing_string)

    def test_save(self):
        savename = 'paragraphssave.odt'
        self.doc.save(savename)
        self.assertTrue(os.path.isfile(savename))
        self.assertTrue(zipfile.is_zipfile(savename))
        os.remove(savename)

        
    @classmethod
    def tearDownClass(cls):
        pass

        

if __name__ == '__main__':
    unittest.main()