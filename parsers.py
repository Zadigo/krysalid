import threading
import itertools
from collections import Counter, deque
from encodings import utf_8
from functools import cached_property
from html.parser import HTMLParser
from io import StringIO, TextIOWrapper
from typing import Union

from krysalid.html_tags import Comment, ElementData, NewLine, Tag
from krysalid.managers import Manager
from krysalid.queryset import QuerySet
from krysalid.utils.iteration import break_when, keep_while


FIRST_LEVEL_TAGS = {'html'}

SECOND_LEVEL_TAGS = {'head', 'body'}

HEAD_TAGS = {'style', 'link', 'meta', 'script'}

CONTENT_TAGS = {'div', 'span', 'main'}


class Algorithm(HTMLParser):
    """Subclasses html.HTMlParser in order to
    process the html tags. This should not be
    subclassed or used directly"""
    
    def __init__(self, extractor, **kwargs):
        self.extractor = extractor
        self.index = 0
        super().__init__(**kwargs)
    
    @property
    def _increase_index(self):
        self.index = self.index + 1
        return self.index

    def handle_startendtag(self, tag, attrs):
        """Handles tags such as <img /> or <img>"""
        self.extractor.self_closing_tag(tag, attrs, position=self.getpos())

    def handle_starttag(self, tag, attrs):
        """Handles tags such as <div>"""
        self.extractor.start_tag(tag, attrs, position=self.getpos())

    def handle_endtag(self, tag):
        """Handles tags such as </div>"""
        self.extractor.end_tag(tag)

    def handle_data(self, data):
        """Handles data within tags 'Kendall' in <span>Kendall</span>"""
        self.extractor.internal_data(data, position=self.getpos())
        
    def handle_comment(self, data):
        """Handles comments"""
        self.extractor.parse_comment(data, position=self.getpos())
        
    def handle_charref(self, name):
        print('charref', name)
        
    def handle_entityref(self, name):
        print('entity', name)
        
    def handle_pi(self, data):
        print('pi', data)
        
    def handle_decl(self, decl):
        print('declaration', decl)
        
    def unknown_decl(self, data):
        print('unknown', data)


class Extractor:
    """The main interface that deals with processing
    each tag sent by the Algorithm"""
    
    HTML_PAGE = None

    def __init__(self, skip_newlines=False, remove_white_space=False, track_line_numbers=False):
        self.algorithm = Algorithm(self)

        self._opened_tags = Counter()
        self._current_tag = None

        # Contains the collected tags
        # and represents the HTML tree
        self.container = deque()
        
        # TODO: Whether to include \n in the
        # collection or not
        self.skip_newlines = skip_newlines

        self.track_line_numbers = track_line_numbers
        # TODO: Whether to keep ' ' data elements
        # in the collection or not
        self.remove_white_space = remove_white_space
        
        self.head = []
        self.body = []
        self.html = ['html', ['head', self.head, '@-head'], ['body', self.body, '@-body'], '@-html']
        self.current_tag_build = []
        self.current_tag_data = []
        self.html_closed = False
        self.head_closed = False
        self.body_closed = False
        self.top_level_tags = FIRST_LEVEL_TAGS | SECOND_LEVEL_TAGS
        self.previous_tag = None
                
    def __iter__(self):
        return iter(self.container)
    
    @cached_property
    def count(self):
        return len(self.container)
    
    def _default_prettifier(self, html) -> str:
        """Function that normalizes the incoming
        html string so that we can deal with a
        standard format"""
        from lxml.etree import tostring
        from lxml.html import fromstring
        
        return tostring(fromstring(html), encoding='unicode', pretty_print=True)
        
    def resolve(self, data):
        self.algorithm.feed(self._default_prettifier(data))
        self.algorithm.close()
        
    def start_tag(self, tag, attrs, **kwargs):
        if not self.head_closed:
            if tag not in self.top_level_tags:
                self.head.append(tag)
        
        if not self.body_closed:
            if tag in CONTENT_TAGS:
                self._opened_tags.update([tag])
                
                if self._current_tag is not None:
                    self.previous_tag = self._current_tag
                
                self._current_tag = tag
                
                if self.current_tag_build:
                    last_item = self.current_tag_build[-1]
                    if isinstance(last_item, str):
                        self.current_tag_build.append([tag])
                    else:
                        last_item.append([tag])
                else:
                    self.current_tag_build.append(tag)
                # self.body.append(tag)
            
    def end_tag(self, tag):
        if tag in self.top_level_tags:
            setattr(self, f"{tag}_closed", True)
            
        if tag in CONTENT_TAGS:
            self._opened_tags.subtract([tag])
            self.body.append(self.current_tag_build)
            self.current_tag_build.clear()
    
    def internal_data(self, data, **kwargs):
        pass
        # if self.current_tag_build:
        #     self.current_tag_data.append(data)
    
    def self_closing_tag(self, tag, attrs, **kwargs):
        if tag in HEAD_TAGS:
            self.head.append(tag)
    
    def parse_comment(self, data: str, **kwargs):
        pass        


class HTMLPageParserDescriptor:        
    def __get__(self, instance, cls=None):
        extractor = Extractor()
        
        data = self.__dict__
        previous_extraction = data.get('extractor', None)
        if previous_extraction is None:
            extractor.resolve(instance._original_page)
            data['extractor'] = extractor
        manager = Manager(extractor)
        return manager
        
        
class HTMLPageParser:
    """The main class used to process the html page.
    It implements the default manager for querying
    the different items"""
    
    objects = HTMLPageParserDescriptor()
    
    def __init__(self, html, defer_resolution=False, skip_newlines=False, track_line_numbers=False):
        string = None
        if isinstance(html, TextIOWrapper):
            # FIXME: Cannot read file if we don't
            # pass utf-8 in open()
            string = html.read()
        elif isinstance(html, StringIO):
            string = html.read()
        elif isinstance(html, bytes):
            string, size = utf_8.decode(html, errors='strict')
        elif isinstance(html, str):
            string = html
        else:
            string = ''
            
        self._original_page = string
        
    @property
    def page_has_content(self):
        return (self._original_page is not None or
                self._original_page != '')
