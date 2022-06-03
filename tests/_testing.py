from krysalid.parser import HTMLPageParser
from krysalid.compiler import Compiler
from krysalid.queryset import QuerySet, RawQueryset
# from krysalid.shortcuts import TableExtractor, TextExtractor, ImageExtractor
# from krysalid.html_tags import Tag

# tag = Tag('img', [], (1, 1))
# print(tag == 'img')
# print('img' in tag)

h = HTMLPageParser.from_file('tests/html/test4.html')
# h = HTMLPageParser.from_file('tests/html/test2.html')
# h = HTMLPageParser.from_file('tests/html/test7.html')cls

# h = HTMLPageParser.from_file('tests/html/tables.html')
# h = HTMLPageParser.from_file('tests/html/simple.html')
# o = h.objects.find(attrs={'id': 'extwaiokist'})
# o = h.objects.find(name='div', attrs={'class': 'kendall'})
# o = h.objects.find('div', attrs={'class': 'top-rankings__title-container'})
# o = h.objects.find_all(name='div')
# o = h.objects.find('div')

# print(o)

c = Compiler(h)
# print(c.get_top_and_lower_indexes('span'))
# r = c.get_tags('span')
# r = c.get_data(newlines=False)
# r = c.map_indexes_by_attributes({'data-name': 'kylie'})
# print(r)

tags = [
    ('ST', 'div', [('class', 'celebrities-1')], (10, 12)), 
        ('DA', '\n', [], (10, 39)),
        ('ST', 'div', [('id', '1')], (11, 16)), 
            ('DA', '\n', [], (11, 28)),
            ('ST', 'span', [], (12, 20)), 
                ('DA', 'Kendall', [], (12, 26)),
            ('ET', 'span', [], (12, 33)),
            
            ('DA', '\n', [], (12, 40)),
            
            ('ST', 'span', [], (13, 20)),
                ('DA', 'Jenner', [], (13, 26)), 
            ('ET', 'span', [], (13, 32)),
            ('DA', '\n', [], (13, 39)), 
        ('ET', 'div', [], (14, 16)),
    ('ET', 'div', [], ())
]

q = RawQueryset(c, tags)
s = q.find_all(name='span')
s = q.find(name='span')
# e = s.find_all(name='span')
print(s)
