from krysalid.parser import HTMLPageParser
from krysalid.compiler import Compiler
from krysalid.queryset import QuerySet


# h = HTMLPageParser.from_file('tests/html/test4.html')

# c = Compiler(h)
# r = c.get_tags('span')
# print(list(r))
# print(h.objects.find('span'))
# h.objects.find_all('span')


page_parser = HTMLPageParser.from_file('tests/html/test4.html')
compiler = Compiler(page_parser)
q = QuerySet(compiler=compiler)
print(len(q.result_cache))
