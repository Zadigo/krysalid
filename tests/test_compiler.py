import unittest
from krysalid.compiler import BaseCompiler
from krysalid.parser import HTMLPageParser
from krysalid.html_tags import Tag

with open('tests/html/simple.html', mode='r') as f:
    parser = HTMLPageParser(f.read())


class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = BaseCompiler(parser)

    # def test_map_indexes(self):
    #     indexes = self.compiler.map_indexes_by_attributes({'id': 'google'})

    def test_map_indexes_by_tag_name(self):
        indexes = self.compiler.map_indexes_by_tag_name('div')
        self.assertIsInstance(indexes, list)
        for index in indexes:
            with self.subTest(index=index):
                self.assertIsInstance(index, tuple)
                self.assertIsInstance(index[0], int)

    def test_get_top_lower_index(self):
        index = self.compiler.get_top_lower_index('div')
        self.assertIsInstance(index, tuple)
        for value in index:
            with self.subTest(value=value):
                self.assertIsInstance(value, int)

    def test_result_iteration(self):
        items = self.compiler.result_iteration()
        for item in items:
            with self.subTest(item=item):
                self.assertIsInstance(item, tuple)
                self.assertIn(item[0], ['ST', 'ET', 'DA'])

    def test_tag_compilation(self):
        tag_tuple = ('ST', 'div', [('id', 'google')], (19, 8))
        obj = self.compiler.compile_tag(tag_tuple, 0)
        self.assertIsInstance(obj, Tag)
        self.assertTrue(obj == 'div')


if __name__ == '__main__':
    unittest.main()
