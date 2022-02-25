# from bs4 import BeautifulSoup
# from importlib_metadata import re
# from krysalid.parsers import HTMLPageParser
import time
# # from bs4 import BeautifulSoup


# f = open('tests/test1.html', encoding='utf-8')
# soup = HTMLPageParser(f)
# body = soup.manager.find_all('div')
# print(body)
# # with open('tests/html_parser/test1.html', encoding='utf-8') as f:
# #     soup = HTMLPageParser(f)
# #     body = soup.manager.find('body')
# #     # print(soup.manager.regex(re.compile(r'^img')))

# #     # b = BeautifulSoup(f, 'html.parser')
# #     # body = b.find('body')
# #     # body.find_all('img')
# f.close()
# e = time.time() - s



from krysalid.parsers import HTMLPageParser


with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
    s = time.time()
    soup = HTMLPageParser(f)
    # tags = soup.manager.find_all('div')
    # tag = tags.find('div')
    # print(tags, tag)
    e = time.time() - s
    print(round(e, 3))




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
