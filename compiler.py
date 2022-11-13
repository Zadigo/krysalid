from collections import Counter, OrderedDict
from functools import cached_property, lru_cache
from io import StringIO

from html_tags import ElementData, NewLine, Tag
from utils import compare_attributes


class Cache:
    """Caches items that were already computed
    by the compiler and returns them if we
    already have them"""
    
    search = {}
    
    def get(self, value, func, args=(), kwargs={}):
        if value in self.search:
            return self.search[value]
        result = func(*args, **kwargs)
        self.search[value] = result
        return result
        
cache = Cache()


class BaseCompiler:
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
    
    # @lru_cache(maxsize=100)
    def map_indexes_by_attributes(self, attrs):
        """Map the indexes of each tags based
        on a matching attribute regardless of their name"""
        top_limits = []
        lower_limits = []
        
        counter = Counter()
        
        for i, tag in enumerate(self.result_iteration()):
            result = compare_attributes(tag[2], attrs)
            if result and 'ST' in tag:
                counter.update([tag[1]])
                top_limits.append(i)
                continue
                        
            if counter[tag[1]] == 1 and 'ET' in tag:
                lower_limits.append(i + 1)
                counter.subtract([tag[1]])

        return [(top_limits[i], lower_limits[i]) for i in range(len(top_limits))]
    
    @lru_cache(maxsize=100)
    def map_indexes_by_tag_name(self, name):
        """Map the indexes of all the tags that
        match the given name"""        
        top_limits = []
        lower_limits = []
        for i, tag in enumerate(self.result_iteration()):
            if name in tag and 'ST' in tag:                
                top_limits.append(i)
                continue
            
            if name in tag and 'ET' in tag:                    
                lower_limits.append(i)
        
        indexes = []
        for i in range(len(top_limits)):
            indexes.append((top_limits[i], lower_limits[i]))
        return indexes
    
    @lru_cache(maxsize=100)
    def get_top_lower_indexes(self, name):
        """From a given tag name get the top and bottom
        indexes of matching parent tags. The final result
        would then allow us to slice the result set in order
        to get a tag and it's children"""
        limits = []
        limit = []
        # Check all open elements and if we have
        # only one item remaining then we know for
        # sure that this would be the closing tag
        # of the top opened one
        counter = Counter({name: 0})
        for i, tag in enumerate(self.result_iteration()):
            # if attrs:
            #     if not tag[2]:
            #         continue
            #     truth_array = map(lambda x: x in tag[2], attrs.items())
            #     if not all(truth_array):
            #         continue
                
            if 'ST' in tag and name in tag:
                # If we have more than one tag
                # opened, then we need to not
                # add any limit since we only
                # want to map the parent tag.
                # This allows us to avoid the
                # trap of mapping nested tags
                # with the same name as the parent
                # e.g. <div>A<div>B</div></div>
                if counter[name] >= 1:
                    continue
                
                counter.update([name])
                limit.append(i)
                continue
            
            if 'ET' in tag and name in tag:
                if counter[name] == 1:
                    limit.append(i + 1)
                    # Add one in order to catch
                    # the end tag which for whatever
                    # reason does not get caught
                    limits.append(limit)
                    limit = []
                counter.subtract([name])

                if counter[name] < 0:
                    counter[name] = 0
                continue
        return limits
    
    def get_top_lower_index(self, name):
        """From a given tag name, get the top and lower
        index (start and end tag) in the result set of the
        *first matching* element which would then allow us to 
        slice it out"""
        tags = self.result_iteration()
        for tag in tags:
            if name in tag:
                break
        top_index = tags.index(tag)
        
        bottom_index = 0
        counter = Counter({name: 0})
        for i, tag in enumerate(tags):
            if name in tag and 'ST' in tag:
                counter.update([name])

            if name in tag and 'ET' in tag:
                bottom_index = i
                counter.subtract([name])

                if counter.get(name) <= 0:
                    break

        return top_index, bottom_index + 1
    
    # def compile_tag(self, name, attrs, coordinates, category, index):
    def compile_tag(self, items, index):
        """Transfoms a tag-tuple in a Python object"""
        category, name, attrs, coordinates = items
        tag_class = self.detect_category(category)
        
        if tag_class.is_string:
            instance = tag_class(name)
        else:
            attrs = OrderedDict(attrs)
            
            instance = tag_class(name, attrs, coordinates)
            if category == 'ET':
                instance.closing_tag = True
        
        instance.index = index
        instance.raw_data = items
        
        return instance
    
    # def build_attrs(self, attrs):
    #     return OrderedDict(attrs)
    
    def detect_category(self, category):
        if category == 'ST':
            return Tag
        if category == 'DA':
            return ElementData
        if category == 'NL':
            return NewLine
        return Tag

    def format_page(self, page):
        from lxml.etree import tostring
        from lxml.html import fromstring
        return tostring(fromstring(page), encoding='unicode', pretty_print=True)
    
    def pre_compile_setup(self, page):
        """Format the HTML page and also determine
        if we are dealing with a snippet or a
        full HTML page"""
        if not '<html>' in page and not '<body>' in page:
            page = f'<html><body>{page}</body></html>'
        # FIXME: Bug with lxml
        # page = self.format_page(page)
        self.clean_page = page
    
    def result_iteration(self):
        """Returns the raw parsed elements on
        the page as a list of tuples: 
        [(category, tag name, attributes, coordinates)]
        """
        return self.page_parser.get_result_cache
    
    
class Compiler(BaseCompiler):
    """Transforms the raw parsed elements from the
    the original parser to Python useable objects"""
    
    @cached_property
    def body(self):
        # Cache the body part of the page
        # in order to improve performance
        # when other functions will be
        # accessing this section
        return self.get_tag('body')
        
    def compile_query(self, query):
        result = []
        tag_name = query.get('tag', None)
        attrs = query.get('attrs', {})
        return self.get_tags(tag_name)
        
    def get_tag(self, name):
        """Return the raw elements of tag.
        Includes the tag and it's children"""
        top_index, bottom_index = self.get_top_lower_index(name)
        return self.result_iteration()[top_index:bottom_index]
    
    def get_tags(self, name):
        """Return all the tags that match the
        given name in a document and their
        internal elements"""
        counter = Counter({name: 0})
        for tag in self.result_iteration():
            if name in tag and 'ST' in tag:
                counter.update([name])
                yield tag
                       
            if name in tag and 'ET' in tag:
                counter.subtract([name])
                yield tag
            
            if counter[name] > 0:
                if 'DA' in tag or 'NL' in tag:
                    yield tag
    
    def get_data(self, newlines=True):
        """Returns all the data tags"""
        for tag in self.result_iteration():
            if 'DA' in tag:
                if not newlines:
                    if '\n' in tag[1]:
                        continue
                yield tag

    # def get_all_text(self, newline=True):
    #     buffer = StringIO(newline='\n')
    #     for item in self.get_data(newlines=newline):
    #         buffer.write(item[1])
    #     buffer.seek(0)
    #     return buffer.read()
