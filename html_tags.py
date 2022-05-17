from functools import total_ordering
from typing import OrderedDict


class BaseTag:
    is_string = False
    
    def __init__(self, name, attrs, coordinates):
        self.name = name
        self.index = 0
        self.coordinates = coordinates
        self.compiler = None
        self._attrs = attrs
        self.closing_tag = False
        # self.closed = False
        # self._previous_sibling = None
        # self._next_sibling = None
        # self._parents = deque()
        # self._children = deque()
        # self._internal_data = deque()
        
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
    
    def deconstruct(self):
        return self.name, list(self.attrs), self.coordinates
    
    def has_attr(self, value):
        return value in self.attrs.keys()
     
    def attrs_as_string(self):
        for key, value in self.attrs.items():
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
