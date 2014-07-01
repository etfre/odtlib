import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from odtlib import odt
from odtlib.tests import specs

class TestOdtlib(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.template_doc = odt.Odt()
        cls.full_doc = odt.Odt(os.path.join(os.path.dirname(__file__), '..', 'templates', 'full.odt'))

    def test_template_files(self):
        self.write_dir = tempfile.mkdtemp()
        template = os.path.join(os.path.dirname(__file__), '..', 'templates', 'new.odt')
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
        paratext = self.full_doc.paragraph_list[0].text
        self.assertEqual(paratext, 'This is a top-secret society! The name should be '
            'something mysterious! Something vaguely ominous and chilling! '
            'Something like, “The Sinister Icy Black Hand of Death Club”!')

    def test_search(self):
        search_result = self.full_doc.search('mysterious')
        self.assertEqual(len(search_result), 1)

    def test_paragraph_setup(self):
        self.assertEqual(len(self.full_doc.paragraph_list), 4)

    def test_replace(self):
        self.full_doc.replace('smock', 'sweatervest')
        self.assertEqual(self.full_doc.paragraph_list[2].text, 'I like my sweatervest. '
            'You can tell the quality of the artist by the quality of his sweatervest. '
            'Actually, I just like to say sweatervest. sweatervest sweatervest '
            'sweatervest sweatervest sweatervest sweatervest.')

    def test_add_paragraph(self):
        paratext = 'Van Gogh would’ve sold more than one painting if he’d put tigers in them.'
        self.full_doc.add_paragraph(paratext)
        self.assertEqual(self.full_doc.paragraph_list[-1].text, paratext)

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