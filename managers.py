import secrets
from collections import deque
from functools import cached_property
from typing import Pattern, Union

from krysalid.exceptions import TagExistsError
from krysalid.html_tags import BaseTag, Tag
from krysalid.queryset import QuerySet
from krysalid.utils.containers import TagsIterable
from krysalid.utils.iteration import (HTML_TAGS, SELF_CLOSING_TAGS,
                                      filter_by_name, filter_by_name_or_attrs,
                                      filter_chunks_by_name)


class Manager:
    def __init__(self, extractor):
        from krysalid.parsers import Extractor
        if not isinstance(extractor, Extractor):
            raise TypeError('Extractor should be an instance of Extractor')
        self._extractor_instance = extractor
        
        # TODO: Test doing all iterations by chunks as
        # opposed to doing one by one values in order
        # to improve global performance especially on
        # large files which can generate 1000s of tags
        self._internal_values = deque()
        # self._internal_values = TagsIterable(extractor)

    def __repr__(self):
        name = self._extractor_instance.__class__.__name__
        return f"<{self.__class__.__name__} for {name}>"

    @cached_property
    def get_title(self) -> Union[str, None]:
        items = filter_by_name(self._extractor_instance, 'title')
        try:
            return list(items)[0]
        except:
            return None
        
    @cached_property
    def count(self):
        return len(self._extractor_instance)

    # @cached_property
    # def links(self):
    #     """Returns all the links contained 
    #     in the HTML page"""
    #     return self.find_all('a')

    # @cached_property
    # def tables(self):
    #     """Returns all the tables contained 
    #     within the HTML page"""
    #     return self.find_all('table')

    def find(self, name: str, attrs: dict = {}) -> Tag:
        """Get a tag by name or attribute. If there are multiple
        tags, the first item of the list is returned"""
        result = filter_by_name_or_attrs(self._extractor_instance, name, attrs)
        try:
            return list(result)[0]
        except IndexError:
            raise TagExistsError(name)

    def find_all(self, name: Union[str, list], attrs: dict = None):
        """Filter tags by name or by attributes"""
        result = filter_by_name_or_attrs(self._extractor_instance, name, attrs)
        return QuerySet.copy(result)
    
    def expressions(self, *args):
        pass
    
    def regex(self, name: Pattern):
        """Filter tags by using a regex pattern"""
        # results = []
        # for chunk in self._internal_values:
        #     for item in chunk:
        #         matched = name.match(item.name)
        #         if matched:
        #             results.append(item)
        def result_set():
            for item in self._internal_values:
                matched = name.match(item.name)
                if matched:
                    yield item
        return QuerySet.copy(result_set())
    
    # def download_images(self, func: Callable):
    #     """Download all the images on the page using
    #     a function that should send a request and return
    #     the image's content as bytes"""
    #     if not callable(func):
    #         raise TypeError('Function should be a callable')
        
    #     image_types = ['jpg', 'jpeg', 'png', 'svg']
        
    #     images = self.find_all('a')
    #     for image in images:
    #         url = image.get_attr('src')
    #         try:
    #             content = func(url)
    #         except:
    #             yield False
    #         else:
    #             if not isinstance(content, bytes):
    #                 raise ValueError('Image content should be bytes')
                
    #             from PIL import Image
    #             instance = Image.open(content)
                
    #             _, extension = url.split('.')
    #             name = f"{secrets.token_hex(n=5)}.{extension}"
    #             with open(name, mode='wb') as f:
    #                 instance.save(f)
    #                 yield True

    # def save(self, filename: str):
    #     pass

    # def live_update(self, url: str=None, html: str=None):
    #     """Fetch a newer version of the html page
    #     using a url or a string"""

    # def insert(self, position: int, tag: Callable):
    #     """Insert a tag at the designed position
    #     within the global collection"""
    #     if not self._has_extractor:
    #         raise TypeError('To use to query with tags, need an extractor')

    #     if not isinstance(tag, BaseTag):
    #         raise TypeError('Tag should be an instance of BaseTag')

    #     self._extractor_instance.container.insert(position, tag)
        
    # def to_representation(self):
    #     html_tree = []
    #     items = self._create_representation()
    #     current_unclosed = None
    #     for item in items:
    #         if item == '\n':
    #             html_tree.append(item)
    #         else:
    #             matched = re.match(r'^\<(\w+)')
    #             if matched:
    #                 if matched.group(1) not in SELF_CLOSING_TAGS:
    #                     current_unclosed = item
    #             else:
    #                 html_tree.append(item)
                    
    #     # from lxml.etree import fromstring
    #     # from lxml.html import tostring
    #     # html = fromstring(html)
    #     # return tostring(html, pretty_print=True, encoding='utf-8')
            
    # def _create_representation(self):
    #     """Show the actual representation of
    #     the Python collection of tags"""
    #     html_tree = []
    #     with self._extractor_instance as tags:
    #         for tag in tags:
    #             if tag.name == 'newline':
    #                 yield '\n'
    #             elif tag.name == 'data':
    #                 yield tag.data
    #             else:
    #                 template = '<{name} {attrs}>'
    #                 yield template.format(name=tag.name, attrs=tag._attrs_to_string)
    #     return html_tree
