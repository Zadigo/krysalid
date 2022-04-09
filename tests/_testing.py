from krysalid.parsers import HTMLPageParser
from krysalid.functions import Q

# with open('tests/html/test4.html', mode='r', encoding='utf-8') as f:
with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
    # s = HTMLPageParser(f)
    # q = s.manager.expressions(Q(a__id__eq='test'), Q(a__id__contains='teest2'))
    # q = s.manager.expressions(Q(a__id='test') & Q(a__id__ne='test2'))
    # q = s.manager.find_all('div')
    # v = q.values('id')
    # print(v.as_tags())
    s = HTMLPageParser(f)
    result = s.objects.find_all('p') 
    print(result.first)
