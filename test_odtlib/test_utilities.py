import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from lxml import etree
from odtlib import text
from test_odtlib import specs
from odtlib.namespace import NSMAP, qn
from odtlib import api
from odtlib.utilities import shared


class TestUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = shared.makeelement('text', 'p', 'Hello world!',
                                  {qn('style', 'name'): '1',
                                   qn('style', 'family'): 'paragraph'})

    def test_remove_substr(self):
        mystr = 'First, I decree double rations for all officers to aid their decision-making capabilities'
        mystr = shared.remove_substr(1, 15, mystr)
        self.assertEqual(mystr, 'F double rations for all officers to aid their decision-making capabilities')

    def test_insert_substr(self):
        mystr = 'Hello world'
        mystr = shared.insert_substr(6, 'there ', mystr)
        self.assertEqual(mystr, 'Hello there world')

    def test_makeelement(self):
        self.assertEqual(self.p.tag, '{{{}}}{}'.format(NSMAP['text'], 'p'))
        self.assertEqual(self.p.text, 'Hello world!')
        self.assertEqual(self.p.attrib.get(qn('style', 'name')), '1')
        self.assertEqual(self.p.attrib.get(qn('style', 'family')), 'paragraph')
        self.assertEqual(len(self.p.attrib), 2)

    def test_compare_elements_true(self):
        p1 = copy.deepcopy(self.p)
        p2 = shared.makeelement('text', 'p', 'Hello world!', {qn('style', 'name'): '2', qn('style', 'family'): 'paragraph'})
        s1 = shared.makeelement('text', 'span', 'Span 1')
        s2 = shared.makeelement('text', 'span', 'Span 2')
        s3 = copy.deepcopy(s1)
        s4 = copy.deepcopy(s2)
        p1.extend([s1, s2])
        p2.extend([s4, s3])
        self.assertTrue(shared.compare_elements(p1, p2, qn('style', 'name')))

    def test_compare_elements_false(self):
        p1 = copy.deepcopy(self.p)
        p2 = shared.makeelement('text', 'p', 'Hello world!')
        self.assertFalse(shared.compare_elements(p1, p2, qn('style', 'name')))
        p2.set(qn('style', 'name'), '2')
        p2.set(qn('style', 'family'), 'paragraph')
        self.assertTrue(shared.compare_elements(p1, p2, qn('style', 'name')))
        s1 = shared.makeelement('text', 'span', 'Span 1')
        s2 = shared.makeelement('text', 'span', 'Span 2')
        s3 = copy.deepcopy(s1)
        s4 = copy.deepcopy(s2)
        s4.text = 'Span 4'
        p1.extend([s1, s2])
        p2.extend([s4, s3])
        self.assertFalse(shared.compare_elements(p1, p2, qn('style', 'name')))

       

        
    @classmethod
    def tearDownClass(cls):
        pass

        

if __name__ == '__main__':
    unittest.main()