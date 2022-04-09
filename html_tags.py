from collections import OrderedDict, deque
from functools import cached_property
from typing import Callable, List, Tuple, Union

from krysalid.queryset import QuerySet
from krysalid.utils.character import deep_clean
from krysalid.utils.iteration import (break_when, drop_while, filter_by_name,
                                      filter_by_name_or_attrs, filter_by_names)


class QueryMixin:
    @property
    def _has_extractor(self):
        return self._extractor_instance is not None

    @property
    def previous_element(self):
        """Returns the element directly before this tag"""
        def filtering_function(x):
            return x.index == self.index - 1
        return break_when(filtering_function, self._extractor_instance)

    @property
    def next_element(self):
        """Returns the element directly next to this tag"""
        def filtering_function(x):
            return x.index == self.index + 1
        return break_when(filtering_function, self._extractor_instance)

    @property
    def contents(self):
        """Returns all the data present
        within the tag"""
        return []

    @property
    def attrs_list(self):
        """Return the attribute keys
        that are present on the tag"""
        return list(self.attrs)

    @cached_property
    def parents(self):
        """List of parents for the tag"""
        return QuerySet.copy(self._parents)

    @cached_property
    def parent(self):
        """Parent for the tag"""
        return self.parents[-1]

    def get_attr(self, name: str) -> Union[str, None]:
        """Returns the value of an attribute"""
        return self.attrs.get(name, None)

    def get_previous(self, name: str):
        """Get the previous element by name on the page
        that appears after this element"""
        try:
            return list(self.get_all_previous(name))[-1]
        except:
            return None

    def get_next(self, name: str):
        """Get the next element by name on this
        page that appears after this tag"""
        try:
            return list(self.get_all_next(name))[0]
        except:
            return None

    def get_all_previous(self, name: str):
        """Get all the previous elements before this
        tag in respect to the name"""
        if not self._has_extractor:
            raise TypeError('To use to query with tags, need an extractor')

        with self._extractor_instance as items:
            for item in items:
                if item.name == name:
                    if item.index < self.index:
                        yield item

    def get_all_next(self, name: str):
        """Get all the next elements after this
        tag in respect to the name"""
        if not self._has_extractor:
            raise TypeError('To use to query with tags, need an extractor')

        with self._extractor_instance as items:
            for item in items:
                if item.name == name:
                    if item.index > self.index:
                        yield item

    def get_children(self, *names):
        """Return children by names contained
        within the tag. If no name is provided,
        returns all of them"""
        items = filter_by_names(self._children, names)
        return QuerySet.copy(items)

    def get_parent(self, name: str):
        """Return a specific parent from list
        of available parents"""
        result = filter_by_name(self.parents, name)
        return list(result)[-1]

    def get_previous_sibling(self, name: str):
        pass

    def get_next_sibling(self, name: str):
        pass

    def delete(self):
        pass

    # def insert_before(self, *tags):
    #     pass

    # def insert_after(self, *tags):
    #     pass
    

class StringMixin:
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return self.data

    def __hash__(self):
        return hash((self.name, self.data, self.index))
    
    def __getattribute__(self, key):
        if key == '_internal_data':
            return None
        
        if key == 'attrs' or key == 'attrs_list':
            return None
        return super().__getattribute__(key)
        # return key
        
    def __eq__(self, value):
        return self.data == value
   
    def __ne__(self, value):
        return self.data != value
    
    def __contains__(self, value):
        return value in self.data
    
    def __add__(self, value):
        return self.data + str(value)
    
    @property
    def string(self):
        return self.data

    @property
    def is_empty_element(self):
        return self.data == '' or self.data == '\n'
    
    # def insert_data(self, data: str):
    #     pass

    # def update_data(self, data: str):
    #     pass

class BaseTag(QueryMixin):
    def __init__(self, name: str, attrs: list=[], extractor: Callable=None):
        self.name = name
        self.closed = False
        self.attrs = self._build_attrs(attrs)    
        self._previous_sibling = None
        self._next_sibling = None
        self._coordinated = []
        self.index = 0
        self._parents = deque()
        self._children = deque()
        self._internal_data = deque()
        
        # from krysalid.extractors import Extractor
        
        # if extractor is not None:
        #     if not isinstance(extractor, Extractor):
        #         raise TypeError('Extractor should be an instance of Extractor')
        self._extractor_instance = extractor
        
    def __repr__(self):
        if self.attrs:
            return f'<{self.name} {self._attrs_to_string}>'
        return f'<{self.name}>'
    
    def __hash__(self):
        attrs = ''.join(self.attrs.values())
        return hash((self.name, self.index, attrs))

    @staticmethod
    def _build_attrs(attrs):
        attrs_dict = OrderedDict()
        for key, value in attrs:
            attrs_dict.setdefault(key, value)
        return attrs_dict
    
    @property
    def string(self):
        # When we have one item, return it,
        # otherwise, with multiple data elements
        # we use a specific logic to determine
        # exactly what to return...
        if len(self._internal_data) == 1:
            return self._internal_data[0]

        # In a case where we have one solid
        # string data an only null strings,
        # then we should return that item
        results = list(drop_while(lambda x: x == 'newline', self._internal_data))
        if results:
            return ' '.join([str(result) for result in results])

        return None
    
    @cached_property
    def _attrs_to_string(self):
        if not self.attrs:
            return ''
        else:
            items = []
            for key, value in self.attrs.items():
                items.append(f'{key}="{value}"')
            return ' '.join(items)


class Tag(BaseTag):
    """Represents an HTML tag"""

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __delitem__(self, key):
        del self.attrs[key]
        
    def __eq__(self, obj):
        logic = [obj.name == self.name, obj.attrs == self.attrs]
        return all(logic)

    def __ne__(self, obj):
        logic = [obj.name != self.name, obj.attrs != self.attrs]
        return all(logic)
    
    def __contains__(self, name_or_obj):
        return name_or_obj in self.children
    
    @property
    def children(self):
        return QuerySet.copy(self._children)
    
    def has_attr(self, name: str):
        return name in self.attrs.keys()

    def get_attr(self, name: str):
        return self.attrs.get(name, None)

    def find(self, name: str, attrs: dict = {}):
        """Find a tag within the children of the tag"""
        result = filter_by_name_or_attrs(self._children, name, attrs)
        try:
            return list(result)[0]
        except:
            return None

    def find_all(self, name: str, attrs: dict = {}, limit: int = None):
        """Find all elements that match a given tag name
        or attribute within the children elements
        of the tag"""
        result = filter_by_name_or_attrs(self._children, name, attrs)
        return QuerySet.copy(result)


class Comment(StringMixin, BaseTag):
    def __init__(self, data: str, extractor: Callable=None):
        super().__init__('comment', extractor=extractor)
        self.data = data
        self.closed = True


class NewLine(StringMixin, BaseTag):
    def __init__(self, data: str='\n', extractor: Callable=None):
        super().__init__('newline', extractor=extractor)
        self.data = data
        self.closed = True
        

class ElementData(StringMixin, BaseTag):
    def __init__(self, data: str, extractor: Callable=None):
        super().__init__('element_data', extractor=extractor)
        self.data = data
        self.closed = True

# div = Tag('div')
# data = ElementData('Kendall')
# div._children = [data]
# print('Kendall' in div)

# div = Tag('div')
# span = Tag('span')
# data = ElementData('Kendall')
# div._children = [div, span, data]
# print('Kendall' in div)


# tag = Tag('div')
# tag._internal_data = [ElementData('kendall'), NewLine(), ElementData('kylie')]
# print(tag.string)

# base_tag = BaseTag('a', [('id', 'name')])
# tag = Tag('a', [('id', 'name')])
# data = ElementData('Some data for you')
# comment = Comment('This is a test comment')
# newline = NewLine()

# tag._internal_data = [data]
# print(tag, data, comment, newline)
# print(hash(comment))
# print(newline.closed)
# print(comment.attrs)
# print(tag.attrs)
# tag['class'] = 'Kendall'
# print(newline.is_empty_element)

# tag = ElementData('Something')
# print(tag.attrs_list)
