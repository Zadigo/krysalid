# from bs4 import BeautifulSoup
# from importlib_metadata import re
# from bs4 import BeautifulSoup
from krysalid.parsers import HTMLPageParser
from krysalid.functions import Q

from krysalid.html_tags import Tag

tags = [Tag('a'), Tag('a', attrs=[('id', 'name')]), Tag('a', attrs=[('id', 'a')])]




f = open('html/test4.html', encoding='utf-8')
soup = HTMLPageParser(f)
body = soup.manager.find_all('div', attrs={'id': '3'})
print(body.explain())
with open('tests/html_parser/test1.html', encoding='utf-8') as f:
    soup = HTMLPageParser(f)
    body = soup.manager.find('body')
    # print(soup.manager.regex(re.compile(r'^img')))

    # b = BeautifulSoup(f, 'html.parser')
    # body = b.find('body')
    # body.find_all('img')
f.close()
# e = time.time() - s



# from krysalid.parsers import HTMLPageParser, Algorithm

# with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
#     s = time.time()
#     soup = HTMLPageParser(f)
#     # tags = soup.manager.find_all('div')
#     # tag = tags.find('div')
#     # print(tags, tag)
#     e = time.time() - s
#     print(round(e, 3))


# from collections.abc import Mapping


# class A(Mapping):
#     def __init__(self):
#         self.elements = (i for i in range(1000000000))
        
#     def __getitem__(self, k):
#         return list(self.elements)[k]
    
#     def __iter__(self):
#         return iter(self.elements)
    
#     def __len__(self):
#         return len(self.elements)

# a = A()
# print(a[100])
