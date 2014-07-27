import unittest
import string
import sys
import os
import shutil
import copy
from lxml import etree
from odtlib import text
from test_odtlib import specs
from odtlib.namespace import NSMAP, qn
from odtlib import api
from odtlib.utilities import shared, textutilities, odt


class TestUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = shared.makeelement('text', 'p', 'Hello world!',
                                  {qn('style:name'): '1',
                                   qn('style:family'): 'paragraph'})

    def test_load_xml_files(self):
        if os.path.exists('dir'):
            shutil.rmtree('dir')
        os.makedirs('dir/level2')
        with open('dir/level2/xml1', 'w') as f:
            f.write('<p><span>Some span text</span></p>')
        with open('dir/improper', 'w') as f:
            f.write('<p><span>Improper xml!</spam></p>')
        files = shared.load_xml_files('dir')
        self.assertEqual(etree.tostring(files['level2/xml1']).decode('utf8'),
                         '<p><span>Some span text</span></p>')
        with self.assertRaises(KeyError):
            files['improper']
        shutil.rmtree('dir')

    def test_get_paragraph_text(self):
        pass

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
        self.assertEqual(self.p.get(qn('style:name')), '1')
        self.assertEqual(self.p.get(qn('style:family')), 'paragraph')
        self.assertEqual(len(self.p.attrib), 2)

    def test_compare_elements_true(self):
        p1 = copy.deepcopy(self.p)
        p2 = shared.makeelement('text', 'p', 'Hello world!', {qn('style:name'): '2', qn('style:family'): 'paragraph'})
        s1 = shared.makeelement('text', 'span', 'Span 1')
        s2 = shared.makeelement('text', 'span', 'Span 2')
        s3 = copy.deepcopy(s1)
        s4 = copy.deepcopy(s2)
        p1.extend([s1, s2])
        p2.extend([s4, s3])
        self.assertTrue(shared.compare_elements(p1, p2, qn('style:name')))

    def test_compare_elements_false(self):
        p1 = copy.deepcopy(self.p)
        p2 = shared.makeelement('text', 'p', 'Hello world!')
        self.assertFalse(shared.compare_elements(p1, p2, qn('style:name')))
        p2.set(qn('style:name'), '2')
        p2.set(qn('style:family'), 'paragraph')
        self.assertTrue(shared.compare_elements(p1, p2, qn('style:name')))
        s1 = shared.makeelement('text', 'span', 'Span 1')
        s2 = shared.makeelement('text', 'span', 'Span 2')
        s3 = copy.deepcopy(s1)
        s4 = copy.deepcopy(s2)
        s4.text = 'Span 4'
        p1.extend([s1, s2])
        p2.extend([s4, s3])
        self.assertFalse(shared.compare_elements(p1, p2, qn('style:name')))


    def test_convert_to_spans(self):
        para = shared.makeelement('text', 'p')
        para.text = 'starting paragraph text.'
        para.set(qn('text:style-name'), 'P1')
        span1 = shared.makeelement('text', 'span', 'Foist span txt')
        tab = shared.makeelement('text', 'tab')
        tab.tail = 'more text after the tab'
        span1.append(tab)
        span1.tail = 'This becomes a new span'
        span1.set(qn('text:style-name'), 'T1')
        para.append(span1)
        odt.convert_to_spans(para)
        self.assertIsNone(para.text)
        self.assertEqual(list(para)[0].tag, qn('text:span'))
        self.assertEqual(list(para)[0].text, 'starting paragraph text.')
        self.assertEqual(list(para)[0].get(qn('text:style-name')), 'P1')
        self.assertEqual(list(para)[1].tag, qn('text:span'))
        self.assertEqual(list(para)[1].text, 'Foist span txt')
        self.assertEqual(list(para)[1].get(qn('text:style-name')), 'T1')
        self.assertIsNone(list(para)[1].tail)
        self.assertEqual(list(list(para)[1])[0].tag, qn('text:tab'))
        self.assertEqual(list(list(para)[1])[0].tail, 'more text after the tab')
        self.assertEqual(list(para)[2].tag, qn('text:span'))
        self.assertEqual(list(para)[2].text, 'This becomes a new span')
        self.assertEqual(list(para)[2].get(qn('text:style-name')), 'P1')
        

    def test_convert_from_spans(self):
        para = shared.makeelement('text', 'p', attributes={qn('text:style-name'): 'P1'})
        span1 = shared.makeelement('text', 'span', 'First!', {qn('text:style-name'): 'P1'})
        span2 = shared.makeelement('text', 'span', 'Second!', {qn('text:style-name'): 'P1'})
        span3 = shared.makeelement('text', 'span', 'Third!', {qn('text:style-name'): 'T1'})
        span4 = shared.makeelement('text', 'span', 'Fourth!', {qn('text:style-name'): 'P1'})
        span5 = shared.makeelement('text', 'span', 'Fifth!', {qn('text:style-name'): 'T2'})
        para.extend([span1, span2, span3, span4, span5])
        odt.convert_from_spans(para)
        self.assertEqual(para.text, 'First!Second!')
        self.assertEqual(list(para)[0].text, 'Third!')
        self.assertEqual(list(para)[0].get(qn('text:style-name')), 'T1')
        self.assertEqual(list(para)[0].tail, 'Fourth!')
        self.assertEqual(list(para)[1].text, 'Fifth!')
        self.assertEqual(list(para)[1].get(qn('text:style-name')), 'T2')
        self.assertEqual(len(list(para)), 2)

       

        
    @classmethod
    def tearDownClass(cls):
        pass

        

if __name__ == '__main__':
    unittest.main()