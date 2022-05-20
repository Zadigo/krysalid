from attr import attr
from krysalid.parser import HTMLPageParser
from krysalid.compiler import Compiler
# from krysalid.queryset import QuerySet
# from krysalid.shortcuts import TableExtractor, TextExtractor, ImageExtractor
# from krysalid.html_tags import Tag

# tag = Tag('img', [], (1, 1))
# print(tag == 'img')
# print('img' in tag)

h = HTMLPageParser.from_file('tests/html/test1.html')
# h = HTMLPageParser.from_file('tests/html/test2.html')
# h = HTMLPageParser.from_file('tests/html/test7.html')
# h = HTMLPageParser.from_file('tests/html/tables.html')
# h = HTMLPageParser.from_file('tests/html/simple.html')
# o = h.objects.find(attrs={'id': 'extwaiokist'})
# o = h.objects.find(name='div', attrs={'class': 'kendall'})
# o = h.objects.find('div', attrs={'class': 'top-rankings__title-container'})
o = h.objects.find_all(name='div').exists()


print(o)

# c = Compiler(h)
# print(c.get_top_and_lower_indexes('span'))
# r = c.get_tags('span')
# r = c.get_data(newlines=False)
# r = c.map_indexes_by_attributes({'data-name': 'kylie'})
# print(r)
