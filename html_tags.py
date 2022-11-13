from collections import OrderedDict
from functools import total_ordering


class NavigationMixin:
    def find_all_next(self, name=None, attrs={}):
        """Finds all the next matching elements
        after the current tag. If name and/or attrs
        return those that match"""

    def find_all_previous(self, name=None):
        """Finds all the previous matching elements
        after the current tag. If name and/or attrs
        return those that match"""
    
    def find_next(self, name=None, attrs={}):
        """Finds the next matching element
        matching the given name"""
    
    def find_previous(self, name=None, attrs={}):
        """Finds the previous matching element
        matching the given name"""

    def find_next_sibling(self, name=None, attrs={}):
        """Finds the next matching sibling"""

    def find_previous_sibling(self, name=None, attrs={}):
        """Finds the previous matching sibling"""

    def find_next_siblings(self, name=None, attrs={}):
        """Finds the next matching siblings"""

    def find_previous_siblings(self, name=None, attrs={}):
        """Finds the previous matching siblings"""
    
    def find_parent(self, name=None, attrs={}):
        """Finds the element's parent"""

    def find_parents(self, name=None, attrs={}):
        """Finds all the parents of the
        current element"""
        
    def get_attribute_list(self, key, default=[]):
        """Returns the attributes as a list"""

    def get_text(self, seperator=None, clean=True):
        """Returns all the text within the
        current element"""


class BaseTag(NavigationMixin):
    is_string = False
    
    TAG_ATTRS_TEMPLATE = "<{name} {attrs}>{content}</{name}>"
    TAG_TEMPLATE = "<{name}>{content}</name>"
    SELF_CLOSING_TAG_TEMPLATE = "<{name} />"
    SELF_CLOSING_TAG_ATTRS_TEMPLATE = "<{name} {attrs} />"
    
    def __init__(self, name, attrs, coordinates):
        self.raw_data = []
        self.name = name
        self.index = 0
        self.coordinates = coordinates
        self.compiler = None
        self._attrs = attrs
        self.closing_tag = False
        self.limits = []
        
    def __repr__(self):
        if self.closing_tag:
            return f"</{self.name}>"
        
        if self.attrs:
            attrs = ' '.join(self.attrs_as_string())
            return f"<{self.name} {attrs}>"
        
        return f"<{self.name}>"
        
    def __hash__(self):
        return hash((self.name, self.index, self.coordinates, self._attrs))
    
    def __eq__(self, value):
        if self._attrs:
            if not isinstance(value, str):
                return self.name == value.name and self.attrs == value.attrs
            
            truth_array = map(lambda x: value == x, self.attrs.values())
            return self.name == value and all(truth_array)
        else:
            return self.name == value
    
    def __contains__(self, value):
        if self._attrs:
            if not isinstance(value, str):
                return self.name in value.name
            
            truth_array = map(lambda x: value in x, self.attrs.values())
            return self.name in value and all(truth_array)
        else:
            return self.name == value
        
    def __getitem__(self, name):
        return self.attrs.get(name, None)
    
    def __setitem__(self, key, value):
        self._attrs.append((key, value))
        
    def __delitem__(self, key):
        candidate = list(filter(lambda x: key in x, self._attrs))
        self._attrs.pop(self._attrs.index(candidate[0]))    
    
    @property
    def attrs(self):
        return OrderedDict(self._attrs)
    
    @property
    def is_opening_tag(self):
        return 'ST' in self.raw_data
    
    @property
    def is_closing_tag(self):
        return 'ET' in self.raw_data
    
    @property
    def is_data(self):
        return 'DA' in self.raw_data
    
    def deconstruct(self):
        return self.name, list(self.attrs), self.coordinates
    
    def has_attr(self, value):
        return value in self.attrs.keys()
     
    def attrs_as_string(self):
        items = list(self.attrs.items())
        
        if not items:
            return None
        
        for key, value in items:
            yield f'{key}="{value}"'
            

class Tag(BaseTag):
    pass

@total_ordering
class StringMixin:    
    is_string = True
    
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return self.data
    
    def __hash__(self) -> int:
        return hash((self.name, self.data, self.index))
    
    def __eq__(self, value):
        return value == self.data
    
    def __contains__(self, value):
        return value in self.data
    
    def __gt__(self, value):
        return len(value) > len(self)
    
    def __len__(self, value):
        return len(value) == len(self)
    
    @property
    def attrs(self):
        return {}
    
    def has_attr(self, name):
        return False


class Comment(StringMixin, BaseTag):
    def __init__(self, data):
        super().__init__('comment', {}, ())
        self.data = data


class NewLine(StringMixin, BaseTag):
    def __init__(self, data='\n'):
        super().__init__('newline', {}, [])
        self.data = data
        
    def __eq__(self, value):
        return value == '\n'
        

class ElementData(StringMixin, BaseTag):
    def __init__(self, data):
        super().__init__('data', {}, [])
        self.data = data


# class HTMLElement(BaseTag):
#     """From a set of raw values, create a
#     python usable object. Useful for methods
#     that need to return one single tag element"""
    
#     def __init__(self, values):
#         if not isinstance(values, list):
#             raise ValueError()
                
#         self._values = values
#         cached_values = values.copy()
#         self.top_boundary = cached_values.pop(0)
#         bottom_boundary = cached_values.pop(-1)
        
#         self._children = cached_values
#         self._content = map(lambda x: 'DA' in x, cached_values)
        
#         super().__init__(self.top_boundary[1], self.top_boundary[2], self.top_boundary[3])

#     @property
#     def is_data(self):
#         return 'DA' in self.top_boundary
    
#     @property
#     def is_tag(self):
#         return 'ST' in self.top_boundary
    
#     @property
#     def is_comment(self):
#         return 'CO' in self.top_boundary
    
#     @property
#     def children(self):
#         from krysalid.queryset import RawQueryset
#         return RawQueryset.clone(self.compiler, data=self._children)
        

# # div = Tag('div', [], (1, 1))
# # div2 = Tag('div', [], (1, 1))
# # div2.closing_tag = True
# # tags = [div, div2]
# # # print(tags)
# # r = ''.join([tag.__repr__() for tag in tags])
# # print(r)
