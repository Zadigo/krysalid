import unittest

from krysalid.html_tags import ElementData
from krysalid.compiler import Compiler
from krysalid.managers import Manager
from krysalid.parser import HTMLPageParser
from krysalid.tests import items


class TestManager(unittest.TestCase):
    def setUp(self):
        page_parser = HTMLPageParser(items.NORMAL_HTML)
        compiler = Compiler(page_parser)
        manager = Manager()
        manager.compiler = compiler
        self.manager = manager
        
    def test_has_content(self):
        self.assertGreater(len(self.manager.compiler.result_iteration()), 0)
        
    # def test_find(self):
    #     tag = self.manager.find('a')
    #     self.assertGreater(len(tag), 0)
    #     # self.assertEqual(tag.name, 'a')
    #     # self.assertEqual(tag.string, 'Question')
        
    # def test_find_all(self):
    #     tags = self.manager.find_all('a')
    #     self.assertEqual(len(tags), 3)
    #     self.assertIsInstance(tags, QuerySet)
        
    #     # Assert that each tag that we got
    #     # are links and not anything else
        
    #     for item in tags:
    #         with self.subTest(item=item):
    #             self.assertEqual(item.name, 'a')
                
    # def test_find_all_with_attrs(self):
    #     # TODO:
    #     tags = self.manager.find_all('a', attrs={'id': 'test'})
        
    #     self.assertEqual(len(tags), 1)
    #     self.assertIsInstance(tags, QuerySet)

    #     # Assert that each tag that we got
    #     # are links and not anything else

    #     for item in tags:
    #         with self.subTest(item=item):
    #             self.assertEqual(item.name, 'a')
                
    # def test_links_property(self):
    #     pass
       
        
if __name__ == '__main__':
    unittest.main()
