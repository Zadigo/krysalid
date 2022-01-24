import unittest

from krysalid.extractors import ImageExtractor
from krysalid.tests.items import IMAGE_HTML


class TestImageExtraction(unittest.TestCase):
    def setUp(self):
        extractor = ImageExtractor()
        extractor.resolve(IMAGE_HTML)
        self.extractor = extractor
        
    def test_number_of_images(self):
        self.assertEqual(self.extractor.container_as_queryset.count, 2)
        
    def test_tags(self):
        with self.extractor as items:
            for item in items:
                self.assertEqual(item.name, 'img')
        
        
if __name__ == '__main__':
    unittest.main()
