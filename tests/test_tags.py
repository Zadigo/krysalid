import unittest
from typing import Generator

from krysalid.html_tags import BaseTag, ElementData, NewLine, Tag, Comment
from krysalid.parsers import HTMLPageParser
from krysalid.queryset import QuerySet
from krysalid.tests.items import SIMPLE_HTML


class TestBaseTag(unittest.TestCase):
    def test_has_attribute(self):
        tag = Tag('a')
        self.assertFalse(tag.has_attr('id'))

    @unittest.expectedFailure
    def test_get_attribute_comment_fail(self):
        # String values have no attrs and therefore
        # should fail at any attempt to get one
        # from them
        comment = Comment('A great comment')
        comment['id']
        
        newline = NewLine()
        newline['id']
        
        data = ElementData('Some simple data')
        data['src']
        
    def test_tag_equality(self):
        link1 = Tag('a')
        link2 = Tag('a', attrs=[('id', 'test')])
        self.assertFalse(link1 == link2)
        
        link1 = Tag('a')
        link2 = Tag('a')
        self.assertTrue(link1 == link2)
        
        link1 = Tag('a', attrs=[('id', 'test')])
        link2 = Tag('a', attrs=[('id', 'test')])
        self.assertTrue(link1 == link2)
        
        data1 = ElementData('Kendall is beautiful')
        data2 = ElementData('Kendall is beautiful')
        data3 = ElementData('Kendall is lovely')
        self.assertTrue(data1 == data2)
        self.assertTrue(data1 != data3)
        
        newline1 = NewLine()
        newline2 = NewLine()
        self.assertTrue(newline1 == newline2)
        
    def test_can_change_attribute_directly(self):
        link = Tag('a')
        link['id'] = 'some-attribute'
        self.assertTrue(link.has_attr('id'))
        
    def test_can_delete_attribute_directly(self):
        link = Tag('a', attrs=[('id', 'some-attribuete')])
        del link['id']
        self.assertFalse(link.has_attr('id'))
        
    def test_contains_on_tags(self):
        # div > span + p
        div = Tag('div')
        span = Tag('span')
        div._children = [span, Tag('p')]
        self.assertTrue(span in div)
        
        data = ElementData('Kendall is a queen')
        self.assertTrue('Kendall' in data)
        
        # TODO: Checking if something exists within
        # a Tag instance using a string fails
        # div._children.extend([data])
        # print('Kendall' in div)
        
    def test_build_attrs(self):
        tag = Tag('a')
        tag.attrs = tag._build_attrs([('id', 'test')])
        self.assertDictEqual(tag.attrs, {'id': 'test'})
        
    def test_attrs_to_string(self):
        # Test that we get the correct formating
        # when converting the dict attrs to string
        # attrs
        tag = Tag('a', attrs=[('id', 'test')])
        self.assertEqual(tag._attrs_to_string, 'id="test"')
        
    def test_find(self):
        # <a><span>something</span></a>
        # a > span{something}
        link = Tag('a')
        span = Tag('span')
        span._internal_data = [ElementData('something')]
        link._children = [span]
        
        result = link.find('span')
        self.assertIsInstance(result, BaseTag)
        self.assertEqual(result.string, 'something')
        
    def test_find_all(self):
        # <a><span>1</span><p>2</p></a>
        # a > span{1} + p{2}
        link = Tag('a')

        span1 = Tag('span')
        span1._internal_data = [ElementData('1')]
        span2 = Tag('span')
        span2._internal_data = [ElementData('2')]
        
        link._children = [span1, span2]
        
        result = link.find_all('span')
        self.assertIsInstance(result, QuerySet)
        
        first_span = result.first
        self.assertEqual(first_span.string, '1')
        
        for item in result:
            with self.subTest(item=item):
                self.assertEqual(item.name, 'span')
            
    def test_can_get_string(self):
        # Test that we can get the string contained
        # within the tag when we call the property
        tag = Tag('a')
        tag._internal_data = [ElementData('Kendall is amazing')]
        self.assertEqual(tag.string, 'Kendall is amazing')
        
        # Test that when we have multiple tags within
        # the given tag, that we get one single string
        tag._internal_data = [ElementData('Kendall is awesome'), NewLine()]
        self.assertEqual(tag.string, 'Kendall is awesome')
        
        # FIXME: This should return the internal strings as one
        # of all the child elements
        tag._internal_data.extend([ElementData('but Kylie is better')])
        self.assertEqual(tag.string, 'Kendall is awesome but Kylie is better')
                
    
class TestQueryFunctions(unittest.TestCase):
    """Test core functionnalities of query
    and navigation functions"""
    
    def setUp(self):
        extractor = HTMLPageParser(SIMPLE_HTML)
        # Use this tag as source tag to evaluate
        # how the functions work
        self.measure_tag = extractor.manager.find('span')
    
    def test_previous_element(self):
        newline = self.measure_tag.previous_element
        self.assertSequenceEqual(newline.name, 'newline')
        
        body = self.measure_tag.previous_element.previous_element
        self.assertSequenceEqual(body.name, 'body')
        
    def test_next_element(self):
        span_data = self.measure_tag.next_element
        self.assertSequenceEqual(span_data.name, 'data')
        self.assertSequenceEqual(span_data.string, '1')
    
    def test_parents(self):
        parents_should_be = ['html', 'body']
        for item in self.measure_tag.parents:
            with self.subTest(item=item):
                self.assertIn(item.name, parents_should_be)
                
    def test_parent(self):
        body = self.measure_tag.parent
        self.assertTrue(body == Tag('body'))
        
    def test_get_attr(self):
        self.assertEqual(self.measure_tag.get_attr('id'), '1')
        
    def test_get_previous(self):
        html = self.measure_tag.get_previous('html')
        self.assertTrue(html == Tag('html'))
        
    def test_get_next(self):
        span = self.measure_tag.get_next('span')
        self.assertTrue(span == Tag('span', attrs=[('id', '2')]))
        self.assertTrue(span.get_attr('id'), '2')
        
    def test_get_all_previous(self):
        expected_previous = ['html']
        generator = self.measure_tag.get_all_previous('html')
        self.assertIsInstance(generator, Generator)
        
        for item in generator:
            with self.subTest(item=item):
                self.assertTrue(item.name in expected_previous)
                
    def test_get_all_next(self):
        expected_previous = ['span']
        generator = self.measure_tag.get_all_next('span')
        self.assertIsInstance(generator, Generator)
        
        for item in generator:
            with self.subTest(item=item):
                self.assertTrue(item.name in expected_previous)
    
    def test_get_parent(self):
        body = self.measure_tag.get_parent('body')
        self.assertEqual(body, Tag('body'))  
        
    def test_attrs_list(self):
        keys = self.measure_tag.attrs_list
        self.assertListEqual(keys, ['id'])
        
    def test_tag_does_not_exist(self):
        # Assert that trying to find a tag that
        # does not exist within the children of
        # the tag returns None
        self.assertIsNone(self.measure_tag.find('a'))
        self.assertEqual(len(self.measure_tag.find_all('a')), 0)
        
        
class TestSpecialTagTests(unittest.TestCase):                
    def test_element_data(self):
        element_data = ElementData('Kendall')
        # Assert that we can compare a raw
        # string to the class
        self.assertTrue(element_data, 'Kendall')
        
        result = element_data + 'Jenner'
        self.assertEqual(result, 'KendallJenner')
        
        data1 = ElementData('Kendall')
        data2 = ElementData('Jenner')
        self.assertEqual(data1 + data2, 'KendallJenner')
        
    def test_string_tag_returns_empty_queryset(self):
        tag = ElementData('Kendall')
        self.assertFalse(tag.get_children().exists())
    
    
if __name__ == '__main__':
    unittest.main()
