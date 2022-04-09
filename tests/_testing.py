# # from bs4 import BeautifulSoup
# # from importlib_metadata import re
# # from krysalid.parsers import HTMLPageParser
# import time
# # # from bs4 import BeautifulSoup


# # f = open('tests/test1.html', encoding='utf-8')
# # soup = HTMLPageParser(f)
# # body = soup.manager.find_all('div')
# # print(body)
# # # with open('tests/html_parser/test1.html', encoding='utf-8') as f:
# # #     soup = HTMLPageParser(f)
# # #     body = soup.manager.find('body')
# # #     # print(soup.manager.regex(re.compile(r'^img')))

# # #     # b = BeautifulSoup(f, 'html.parser')
# # #     # body = b.find('body')
# # #     # body.find_all('img')
# # f.close()
# # e = time.time() - s



# from krysalid.parsers import HTMLPageParser

# # with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
# #     s = time.time()
# #     soup = HTMLPageParser(f)
# #     # tags = soup.manager.find_all('div')
# #     # tag = tags.find('div')
# #     # print(tags, tag)
# #     e = time.time() - s
# #     print(round(e, 3))


# # from collections.abc import Mapping


# # class A(Mapping):
# #     def __init__(self):
# #         self.elements = (i for i in range(1000000000))
        
# #     def __getitem__(self, k):
# #         return list(self.elements)[k]
    
# #     def __iter__(self):
# #         return iter(self.elements)
    
# #     def __len__(self):
# #         return len(self.elements)

# # a = A()
# # print(a[100])

# import time

# with open('./tests/html/test1.html', mode='r', encoding='utf-8') as f:
#     h = f.read()
#     s = time.time()
#     p = HTMLPageParser(h)
#     q = p.manager.find_all('p').values('id', 'class', include_fields=True)
#     print(q)
#     e = time.time() - s

# print(round(e, 3))
# from krysalid.parsers import HTMLPageParser
# from krysalid.functions import Q

# # with open('tests/html/test4.html', mode='r', encoding='utf-8') as f:
# with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
#     # s = HTMLPageParser(f)
#     # q = s.manager.expressions(Q(a__id__eq='test'), Q(a__id__contains='teest2'))
#     # q = s.manager.expressions(Q(a__id='test') & Q(a__id__ne='test2'))
#     # q = s.manager.find_all('div')
#     # v = q.values('id')
#     # print(v.as_tags())
#     s = HTMLPageParser(f)
#     result = s.objects.find_all('p')

from functools import lru_cache
from krysalid.html_tags import Tag, ElementData, NewLine, Comment

IDENTIFIER_DATA = '@krysalid-data'
IDENTIFIER_TAG = '@krysalid-tag'
IDENTIFIER_COMMENT = '@krysalid-commment'
IDENTIFIER_NEWLINE = '@krysalid-newline'

HTML_PAGE = ['html', ['body', '-body'], '-html']
HTML_PAGE2 = ['div', '+something', '-div']
item_to_find = 'body'

search = []


class Renderer:
    def __init__(self, page, limit_to='html'):
        self.page = page
        self.limit_to = limit_to
        self._cache = []
    
    def __repr__(self):
        klass_dict = self.__dict__
        html = klass_dict.get('result', None)
        if html is None:
            self.render()
            klass_dict['result'] = self._cache
        return str(klass_dict['result'])
    
    def _get_tag(self, item):
        if item.startswith('+'):
            return ElementData(item)
        else:
            instance = Tag(item)
            if item.startswith('-'):
                instance.closed = True
            return instance
    
    @property
    def has_html(self):
        return 'html' in self.page
    
    def _rebuild_fragment(self, fragment):
        return ['html', ['body', fragment, '@-body'], '@-html']
    
    def end_tag(self, tag):
        return f"-{tag}"

    def drop_while(self, name, items):
        results = []
        for item in items:
            if name in item or self.end_tag(name) in item:
                continue
            results.extend(item)
        return results

    @lru_cache(maxsize=5)
    def level_one(self):
        # <html>...</html>
        for i, item in enumerate(HTML_PAGE):
            yield i, item
            
    def level_two(self):
        # <head>...</head><body>...</body>
        LEVEL_TWO_TAGS = {'head', 'body'}
        for item in self.level_one():
            index, tags = item
            name = item[1][0]
            if name in LEVEL_TWO_TAGS:
                yield {'parent': 0, 'name': name, 'tags': tags}
                
    def decompose_inner(self, elements, tag_name):
        candidates = []
        for element in elements:
            if not element['name'] == tag_name:
                continue
            tags = element['tags']
            for inner_item in tags:
                # if inner_item == tag_name or inner_item == self.end_tag(tag_name):
                #     continue
                candidates.append(inner_item)
        return candidates

    def render_from_list(self, items):
        for item in items:
            if isinstance(item, list):
                return self.render_from_list(items)
            elif isinstance(item, str):
                yield self._get_tag(item)

    def render(self):
        result = []
        # current_element = None
        
        if self.limit_to == 'html':
            tags = self.level_one()
        else:
            tags = self.level_two()
            
        decomposed = self.decompose_inner(tags, 'body')
        
        for item in decomposed:
            if isinstance(item, str):   
                result.append(self._get_tag(item))
            elif isinstance(item, list):
                results = list(self.render_from_list(item))
                result.extend(results)
            # current_element = None
        self._cache = result
            
            
instance = Renderer(HTML_PAGE, limit_to='body')
print(instance)
