import pathlib
from encodings import utf_8
from functools import cached_property
from html.parser import HTMLParser
from io import StringIO, TextIOWrapper

from compiler import Compiler
from exceptions import PathNotExistsError
from managers import Manager


class Algorithm(HTMLParser):    
    def __init__(self, **kwargs):
        self.container = []
        super().__init__(**kwargs)

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
        """Handles data e.g. 'Kendall' in <span>Kendall</span>"""
        # Special case for newlines where
        # we return a stripped version
        if '\n' in data:
            data = data.strip(' ')
            if data == '\n':
                data = '\n'
        self.container.append(('DA', data, [], self.getpos()))
        
    def handle_comment(self, data):
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
        # Optimize page parsing by skipping 
        # certain CDATA unecessary tags like 
        # style and script tags
        # self.optimize = optimize
        self.cached_page = ''
        self.encoding = encoding
        
        if isinstance(html, str):
            self.cached_page = html
        
        # if isinstance(html, TextIOWrapper):
        #     html.encoding = 'utf-8'
        #     # FIXME: Cannot read file if we don't
        #     # pass utf-8 in open()
        #     self.cached_page = html.read()
        # elif isinstance(html, StringIO):
        #     self.cached_page = html.read()
        # elif isinstance(html, bytes):
        #     self.cached_page, size = utf_8.decode(html, errors='strict')
        # elif isinstance(html, str):
        #     self.cached_page = html
            
        self.algorithm = self.algorithm_class(**kwargs)
        self.compiler = self.compiler_class(self)
            
    def __repr__(self):
        return f"<{self.__class__.__name__}[{len(self.get_result_cache)}]>"
    
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
        path = cls.check_path(path)

        with open(path, mode='r', encoding=encoding) as f:
            content = f.read()
            instance = cls(html=content)
            return instance
    
    # @classmethod
    # def from_directory(cls, path, encoding='utf-8'):
    #     path = cls.preconfigure_path(path)
    #     files = path.glob('**/*')
    #     valid_html_files = (
    #         item for item in files 
    #             if item.is_file() and item.suffix == '.html'
    #     )
    
    @staticmethod
    def check_path(path):
        path = pathlib.Path(path)

        if not path.exists():
            raise PathNotExistsError(path=path)

        if not path.is_file():
            raise ValueError('Path does not seems to point towards a file')

        if not path.suffix == '.html':
            raise ValueError('File is not an HTML file')
        
        return path
    
    def parse_page(self):
        """Get the list of tags as list of
        tuples to be used by the compiler"""
        self.compiler.pre_compile_setup(self.cached_page)
        self.algorithm.feed(self.compiler.clean_page)
        self.algorithm.close()
