import unittest

from krysalid.parser import HTMLPageParser
from krysalid.tests import items


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.parser = HTMLPageParser(items.NORMAL_HTML)
        
    def test_can_resolve(self):
        result = self.parser.get_result_cache
        self.assertGreater(len(result), 0)
        self.assertTrue(self.parser.has_content)
        self.assertTupleEqual(result[0], ('ST', 'html', [], (1, 0)))
        
        
if __name__ == '__main__':
    unittest.main()
