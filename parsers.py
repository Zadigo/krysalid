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


class Algorithm(HTMLParser):
    """Subclasses html.HTMlParser in order to
    process the html tags. This should not be
    subclassed or used directly"""
    
    def __init__(self, extractor, **kwargs):
        # TODO: Should be an instance of extractor?
        # from krysalid.extractors import Extractor
        # if not isinstance(extractor, Extractor):
        #     raise TypeError('Extractor should be an instance of extractor')
        self.extractor = extractor
        self.index = 0
        super().__init__(**kwargs)
    
    @property
    def _increase_index(self):
        self.index = self.index + 1
        return self.index

    def handle_startendtag(self, tag, attrs):
        """Handles tags such as <img /> or <img>"""
        self.extractor.self_closing_tag(tag, attrs, position=self.getpos(), index=self._increase_index)

    def handle_starttag(self, tag, attrs):
        """Handles tags such as <div>"""
        self.extractor.start_tag(tag, attrs, position=self.getpos(), index=self._increase_index)

    def handle_endtag(self, tag):
        """Handles tags such as </div>"""
        self.extractor.end_tag(tag)

    def handle_data(self, data):
        """Handles data within tags 'Kendall' in <span>Kendall</span>"""
        self.extractor.internal_data(data, position=self.getpos(), index=self._increase_index)
        
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
        
        # Stores all the positions of
        # the items that were parsed
        self._coordinates = []
        
        # TODO: Whether to include \n in the
        # collection or not
        self.skip_newlines = skip_newlines

        self.track_line_numbers = track_line_numbers
        # TODO: Whether to keep ' ' data elements
        # in the collection or not
        self.remove_white_space = remove_white_space

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.container)})"

    def __getitem__(self, index):
        return self.container[index]
    
    def __iter__(self):
        return iter(self.container)
        # return self._iter_chunks()
        
    def __len__(self):
        return len(self.container)

    def __enter__(self, **kwargs):
        return self.container

    def __exit__(self, *args, **kwargs):
        return False

    @cached_property
    def container_as_queryset(self):
        """Retunrns the container as
        a QuerySet instance"""
        return QuerySet.copy(self.container)

    @property
    def _get_previous_tag(self):
        try:
            return self.container[-2]
        except IndexError:
            # There is no previous so
            # just return None
            return None

    @staticmethod
    def _reformat_fragment(fragment):
        """When a string comes as a fragment of full
        document, recompose the whole structure"""
        return f"<html><head></head><body>{fragment}</body></html>"
    
    def _iter_chunks(self, chunk_size=100):
        """Divide each tags in chunks for
        optimized iteration"""
        iterator = iter(self.container)
        while True:
            chunk = tuple(itertools.islice(iterator, chunk_size))
            if not chunk:
                break
            yield chunk
        
    def _get_default_prettifier(self, html: str) -> str:
        """Function that normalizes the incoming
        html string so that we can deal with a
        standard format"""
        from lxml.etree import tostring
        from lxml.html import fromstring
        
        return tostring(fromstring(html), encoding='unicode', pretty_print=True)
    
    def _add_coordinates(self, tag, coordinates):
        """Reference each tag with an index number
        and eventually the line position returned
        by the HTMLParser"""
        tag._coordinates = coordinates.get('position')
        tag.index = coordinates.get('index')
        
        if self.track_line_numbers:
            self._coordinates.append(coordinates)

    def recursively_add_tag(self, instance):
        """Adds the current tag recursively 
        to all the previous tags that are open"""
        # TODO: Optimize iteration on this section
        # because it is getting called multiple times
        # and can probably slow down as more tags
        # are being added to the container
        # for i in range(0, len(self.container) - 1):
        #     tag = self.container[i]
        #     if not tag.closed:
        #         tag._children.append(instance)
        for chunk in self._iter_chunks():
            for item in chunk:
                if not item.closed:
                    item._children.append(instance)

    def resolve(self, html: str):
        """Entrypoint for transforming each html 
        string tags into Python objects"""
        
        self.HTML_PAGE = self._get_default_prettifier(html)
        # self.HTML_PAGE = html
        
        # TEST: From this section onwards try
        # to figure out the performance of the
        # the code that runs before and after
        # using the Python feed
        self.algorithm.feed(self.HTML_PAGE)
        self.algorithm.close()
        
    def start_tag(self, tag, attrs, **kwargs):
        self._opened_tags.update([tag])

        # Iterate over the container
        # in order to find tags that are not
        # closed. Using this technique, we will
        # then know that these tags are the parents
        # of the current tag by definition
        
        # TEST: Check if not evaluating the parents
        # by calling list on the generator improves
        # performance
        unclosed_tags = keep_while(lambda x: not x.closed, self.container)
        # print(tag, unclosed_tags)

        klass = Tag(tag, attrs, extractor=self)
        
        # Add the newly created tag to
        # the children list of the
        # all the previous opened tags
        self.recursively_add_tag(klass)
        self.container.append(klass)
        self._current_tag = klass

        klass._parents = unclosed_tags
        
        # The sibling is the previous
        # closed tag from the list
        # previous_tag = self._get_previous_tag
        # if previous_tag is not None:
        #     if previous_tag.name == 'tag' and previous_tag.closed:
        #         print('previous', previous_tag)

        if self.track_line_numbers:
            self._add_coordinates(klass, kwargs)
        
        # print(tag, kwargs)
        # print(tag, klass)

    def end_tag(self, tag):
        # TODO: Try to optimize iteration
        # on this section
        def filter_function(item):
            return item.name == tag and not item.closed
        tag_to_close = break_when(filter_function, self.container)
        tag_to_close.closed = True
        # print('/', tag, tag_to_close)

    def internal_data(self, data, **kwargs):
        data_instance = None
        # \n is sometimes considered as
        # data witthin a tag we need to 
        # deal with strings that
        # come as "\n   " and represent
        # them as NewLine if necessary
        if '\n' in data:
            element = data.strip(' ')
            if element == '\n':
                data_instance = NewLine(extractor=self)
            else:
                # TODO: Elements such as \n\n or ' ' need to be dealt
                # with because they are currently treated by default
                # as ElementData
                data_instance = ElementData(element, extractor=self)
        else:
            # TODO: Elements such as \n\n or ' ' need to be dealt
            # with because they are currently treated by default
            # as ElementData
            data_instance = ElementData(data, extractor=self)

        # print('>', data_instance, kwargs.get('position'))
        
        if self.track_line_numbers:
            self._add_coordinates(data_instance, kwargs)

        try:
            # Certain tags do not have an internal_data
            # attribute and will raise an error because 
            # technically they are not supposed to contain
            # data. In that specific case, if the current tag
            # is a data element, just skip on error
            self._current_tag._internal_data.append(data_instance)
        except:
            pass
        
        self.recursively_add_tag(data_instance)
        self.container.append(data_instance)
        # print(data)

    def self_closing_tag(self, tag, attrs, **kwargs):
        """Handle tags that are self closed example <link>, <img>"""
        self._opened_tags.update([tag])

        klass = Tag(tag, attrs, extractor=self)
        self.container.append(klass)
        self._current_tag = klass
        klass.closed = True

        self.recursively_add_tag(klass)

        if self.track_line_numbers:
            self._add_coordinates(klass, kwargs)
        
    def parse_comment(self, data: str, **kwargs):
        klass = Comment(data)
        
        self.recursively_add_tag(klass)
        
        self.container.append(klass)
        self._current_tag = klass
        klass.closed = True

        if self.track_line_numbers:
            self._add_coordinates(klass, kwargs)


class HTMLPageParserDescriptor:
    def __init__(self):
        self.result = None
        
    def __get__(self, instance, cls=None):
        extractor = Extractor(skip_newlines=instance.skip_newlines)
        
        data = self.__dict__
        previous_extraction = data.get('extractor', None)
        if previous_extraction is None:
            thread = threading.Thread(target=extractor.resolve, kwargs={'html': instance._original_page})
            # extractor.resolve(instance._original_page)
            thread.start()
            thread.join()
            data['extractor'] = extractor
        manager = Manager(extractor)
        return manager
        
        
class HTMLPageParser:
    """The main class used to process the html page.
    It implements the default manager for querying
    the different items"""
    
    objects = HTMLPageParserDescriptor()
    
    def __init__(self, html: Union[str, bytes, TextIOWrapper, StringIO],
                 defer_resolution: bool=False, skip_newlines: bool=False,
                 track_line_numbers: bool=False):
        # self.manager = Manager(self)
        # super().__init__(skip_newlines=skip_newlines, track_line_numbers=track_line_numbers)

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
        
        # if not defer_resolution:
        #     self.resolve(self._original_page)
        
    @property
    def page_has_content(self):
        return (
            self._original_page is not None or
            self._original_page != ''
        )
