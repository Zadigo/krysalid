from krysalid.parsers import HTMLPageParser

with open('tests/html/test4.html', mode='r', encoding='utf-8') as f:
    s = HTMLPageParser(f)
    q = s.manager.find_all('div')
    v = q.values('id')
    print(v.as_tags())
