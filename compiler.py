from typing import OrderedDict
from krysalid.html_tags import Tag, ElementData

class BaseCompiler:
    pass


class Compiler(BaseCompiler):
    """Transforms the raw parsed elements from the
    the original parser to Python useable objects"""
    def __init__(self, page_parser):
        self.clean_page = None
        self.page_parser = page_parser
        
    def clone(self):
        # Create a new individual instance of
        # the compiler e.g. for querysets
        klass = type(self.__class__.__name__, (BaseCompiler,), {})
        setattr(klass, '__init__', self.__init__)
        instance = klass(self.page_parser)
        instance.__dict__ = self.__dict__.copy()
        setattr(instance, 'clean_page', self.clean_page)
        return instance
    
    def compile_query(self, query):
        result = []
        tag_name = query.get('tag', None)
        attrs = query.get('attrs', {})
        
        
    def compile_tag(self, name, attrs, coordinates, category, index):
        tag_class = self.detect_category(category)
        if tag_class.is_string:
            instance = tag_class(name)
            return instance
        else:
            attrs = self.build_attrs(attrs)
            
            instance = tag_class(name, attrs, coordinates)
            if category == 'ET':
                instance.closing_tag = True
            instance.index = index
            return instance
    
    def build_attrs(self, attrs):
        return OrderedDict(attrs)
    
    def detect_category(self, category):
        if category == 'ST':
            return Tag
        if category == 'DA':
            return ElementData
        return Tag
    
    def format_page(self, page):
        from lxml.etree import tostring
        from lxml.html import fromstring
        return tostring(fromstring(page), encoding='unicode', pretty_print=True)
    
    def pre_compile_setup(self, page):
        """Format the HTML page and """
        page = self.format_page(page)
        self.clean_page = page
    
    def result_iteration(self):
        """Returns the raw parsed elements on
        the page as a list of tuples: [(category, tag name, 
        attributes, coordinates)]"""
        return self.page_parser.get_result_cache
        
    def get_top_and_lower_indexes(self, name):
        """From a given tag name, get the top and lower
        index (start and end tag) off the result set"""
        tags = self.result_iteration()
        for tag in tags:
            if name in tag:
                break
        top_index = tags.index(tag)
        
        for tag in tags:
            if name in tag and 'ET' in tag:
                break
        bottom_index = tags.index(tag) + 1
        
        return top_index, bottom_index
    
    def get_tag(self, name):
        top_index, bottom_index = self.get_top_and_lower_indexes(name)
        return self.result_iteration()[top_index:bottom_index]
    
    def get_tags(self, name):
        for tag in self.result_iteration():
            if name in tag:
                yield tag
                
