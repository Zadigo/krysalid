from parser import HTMLPageParser

with open('tests\html\simple.html') as f:
    h = HTMLPageParser(f.read())
    # q = h.objects.find('div')
    # q = h.objects.find('div', attrs={'id': 'google'})
    # print(q)

    w = h.compiler.get_tags('div')
    print(h.compiler.compile_tag(list(w)[0], 0))
