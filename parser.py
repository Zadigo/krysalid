from encodings import utf_8
from functools import cached_property
from html.parser import HTMLParser
from io import StringIO, TextIOWrapper
import pathlib
from krysalid.managers import Manager
from krysalid.compiler import Compiler

 
class Algorithm(HTMLParser):    
    def __init__(self, **kwargs):
        self.container = []
        super().__init__(**kwargs)
    
    @property
    def _increase_index(self):
        self.index = self.index + 1
        return self.index

    def handle_startendtag(self, tag, attrs):
        """Handles tags such as <img /> or <img>"""
        self.container.append(('SE', tag, attrs, self.getpos()))

    def handle_starttag(self, tag, attrs):
        """Handles tags such as <div>"""
        self.container.append(('ST', tag, attrs, self.getpos()))

    def handle_endtag(self, tag):
        """Handles tags such as </div>"""
        self.container.append(('ET', tag, [], self.getpos()))

    def handle_data(self, data):
        """Handles data within tags 'Kendall' in <span>Kendall</span>"""
        self.container.append(('DA', data, [], self.getpos()))
        
    def handle_comment(self, data):
        """Handles comments"""
        self.container.append(('CO', data, [], self.getpos()))
        
    def handle_charref(self, name):
        print('charref', name)
        
    def handle_entityref(self, name):
        print('entity', name)
        
    def handle_pi(self, data):
        print('pi', data)
        
    def handle_decl(self, decl):
        self.container.append(('DEC', decl, [], self.getpos()))
        
    def unknown_decl(self, data):
        print('unknown', data)


class HTMLPageParser:
    algorithm_class = Algorithm
    compiler_class = Compiler
    objects = Manager()
    
    def __init__(self, html=None, encoding='utf-8', **kwargs):
        self.cached_page = ''
        
        if isinstance(html, TextIOWrapper):
            html.encoding = 'utf-8'
            # FIXME: Cannot read file if we don't
            # pass utf-8 in open()
            self.cached_page = html.read()
        elif isinstance(html, StringIO):
            self.cached_page = html.read()
        elif isinstance(html, bytes):
            self.cached_page, size = utf_8.decode(html, errors='strict')
        elif isinstance(html, str):
            self.cached_page = html
            
        self.algorithm = self.algorithm_class(**kwargs)
        self.compiler = self.compiler_class(self)
        self.encoding = encoding
            
    def __repr__(self):
        return f"<{self.__class__.__name__}[]>"
    
    @property
    def has_content(self):
        return all([
            self.cached_page is not None,
            self.cached_page != ''
        ])
    
    @cached_property
    def get_result_cache(self):
        self.parse_page()
        return self.algorithm.container
    
    @classmethod
    def from_file(cls, path, encoding='utf-8'):
        path = pathlib.Path(path)
        
        if not path.exists():
            raise ValueError('Path does not exist')
        
        if not path.is_file():
            raise ValueError('Is not a file')

        with open(path, mode='r', encoding=encoding) as f:
            content = f.read()
            instance = cls(html=content)
            return instance
    
    def parse_page(self):
        """Get the list of tags as list of
        tuples to be used by the compiler"""
        # Before reading the page, ensure that
        # the page is correctly formatted
        self.compiler.pre_compile_setup(self.cached_page)
        self.algorithm.feed(self.compiler.clean_page)
