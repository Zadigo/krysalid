from krysalid.parser import HTMLPageParser
from krysalid.compiler import Compiler
from krysalid.queryset import QuerySet
from krysalid.shortcuts import TableExtractor, TextExtractor, ImageExtractor
from krysalid.html_tags import Tag

# tag = Tag('img', [], (1, 1))
# print(tag == 'img')
# print('img' in tag)

# h = HTMLPageParser.from_file('tests/html/test4.html')
# h = HTMLPageParser.from_file('tests/html/tables.html')
h = HTMLPageParser.from_file('tests/html/test1.html')

# c = Compiler(h)
# r = c.get_tags('span')
# print(list(r))
# print(h.objects.find('span'))
# h.objects.find_all('span')


# compiler = Compiler(page_parser)
# q = QuerySet(compiler=compiler)
# print(len(q.result_cache))

# tables = TableExtractor(h)
# print(tables)

# text = TextExtractor(h, skip_newlines=True)
# print(text)

# images = ImageExtractor(h, skip_newlines=True)
# print(images)
