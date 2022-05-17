import unittest

from krysalid.html_tags import ElementData, Tag
from krysalid.queryset import QuerySet
from krysalid.parser import HTMLPageParser
from krysalid.compiler import Compiler


class TestQueryset(unittest.TestCase):
    def setUp(self):
        page_parser = HTMLPageParser.from_file('tests/html/test4.html')
        compiler = Compiler(page_parser)
        self.queryset = QuerySet(compiler=compiler)

    def test_result_cache(self):
        self.assertIsNone(self.queryset.result_cache)
        # NOTE: Cannot call len on the result cache
        # self.assertEqual(len(self.queryset.result_cache), 0)
        
        # NOTE: The queryset is evaluated only when __len__
        # or __repr__ or __str__ are called which in turn
        # calls fetch_all()
        self.queryset.fetch_all()
        self.assertIsNotNone(self.queryset.result_cache)
        # self.assertGreater(len(self.queryset.result_cache), 0)
        
    # def test_exists(self):
    #     self.assertTrue(self.queryset.exists())
        
    def test_count(self):
        self.assertEqual(self.queryset.count, 4)
        
    # def test_first(self):
    #     self.assertEqual(self.queryset.first.name, 'html')
        
    # def test_last(self):
    #     self.assertEqual(self.queryset.last.name, 'data')
        
    # def test_find_all(self):
    #     result = self.queryset.find_all('span')
    #     for item in result:
    #         with self.subTest(item=item):
    #             self.assertTrue(item.name == 'span')
                
    # def test_exclude(self):
    #     result = self.queryset.exclude('span')
    #     for item in result:
    #         with self.subTest(item=item):
    #             self.assertTrue(item.name != 'span')
                
    # def test_distinct(self):
    #     pass
    
    # def test_values(self):
    #     result = self.queryset.values('string')
    #     self.assertListEqual(list(result), [[None], [None], ['Something'], ['Something']])
    
    #     # When a field does not exist on the instance
    #     result = self.queryset.values('name')
    #     print(result)

    # def test_dates(self):
    #     pass
    
    # def test_union(self):
    #     pass
    
    # def test_contains(self):
    #     result = self.queryset.contains('span')
    #     self.assertTrue(result)
        
    #     result = self.queryset.contains('a')
    #     self.assertFalse(result)
    
    # def test_explain(self): 
    #     pass
    
    # def test_generator(self): 
    #     pass
                

if __name__ == '__main__':
    unittest.main()
