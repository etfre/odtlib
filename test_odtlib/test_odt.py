import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
import odtlib
from test_odtlib import specs
from odtlib import api

class TestOdtlib(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.template_doc = api.Odt()
        cls.full_doc = api.Odt(os.path.join(os.path.dirname(__file__), '..', 'odtlib', 'templates', 'full.odt'))

    def test_template_files(self):
        self.write_dir = tempfile.mkdtemp()
        template = os.path.join(os.path.dirname(__file__), '..', 'odtlib', 'templates', 'new.odt')
        with zipfile.ZipFile(template, 'r') as odtzip:
            odtzip.extractall(self.write_dir)
        template_files = copy.deepcopy(specs.TEMPLATE_FILES)
        for root, dirs, files in os.walk(self.write_dir):
            for filename in files:
                abspath = os.path.join(root, filename)
                relpath = os.path.relpath(abspath, self.write_dir)
                self.assertIn(relpath, template_files)
                template_files.remove(relpath)
        self.assertEqual(len(template_files), 0)
        shutil.rmtree(self.write_dir)

    def test_paragraph_text_getter(self):
        paratext = self.full_doc.paragraphs[0].text
        self.assertEqual(paratext, 'This is a top-secret society! The name should be '
            'something mysterious! Something vaguely ominous and chilling! '
            'Something like, “The Sinister Icy Black Hand of Death Club”!')

    def test_paragraph_text_setter(self):
        para = self.full_doc.paragraphs[2]
        para.text += ' Or else!'
        self.assertEqual(para.text, "Don't sell the bike shop, Orville. Or else!")
        para.text = 'It builds character. Keep at it.'
        self.assertEqual(para.text, 'It builds character. Keep at it.')

    def test_search(self):
        search_result = self.full_doc.search('mysterious')
        self.assertEqual(len(search_result), 1)

    def test_replace(self):
        self.full_doc.replace('smock', 'beret')
        self.assertEqual(self.full_doc.paragraphs[4].text, 'I like my beret. '
            'You can tell the quality of the artist by the quality of his beret. '
            'Actually, I just like to say beret. beret beret beret beret beret '
            'beret.')

    def test_append_paragraph(self):
        self.assertEqual(len(self.full_doc.paragraphs), 5)
        paratext = 'Van Gogh would’ve sold more than one painting if he’d put tigers in them.'
        self.full_doc.paragraphs.append(paratext)
        self.assertEqual(self.full_doc.paragraphs[-1].text, paratext)
        del self.full_doc.paragraphs[-1]
        self.assertEqual(len(self.full_doc.paragraphs), 5)

    def test_template_save(self):
        savename = 'templatesave.odt'
        self.template_doc.save(savename)
        self.assertTrue(os.path.isfile(savename))
        self.assertTrue(zipfile.is_zipfile(savename))
        os.remove(savename)

    def test_save(self):
        savename = 'fullsave.odt'
        self.full_doc.save(savename)
        self.assertTrue(os.path.isfile(savename))
        self.assertTrue(zipfile.is_zipfile(savename))
        os.remove(savename)
        
    @classmethod
    def tearDownClass(cls):
        pass

        

if __name__ == '__main__':
    unittest.main()