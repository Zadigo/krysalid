

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
        attrs = ' '.join(self.attrs_as_string())
        return f"<{self.name} {attrs}>"
        
    def __hash__(self):
        return hash((self.name, self.index, self.coordinates, self._attrs))
    
    def attrs_as_string(self):
        for key, value in self._attrs.items():
            yield f"{key}={value}"


class Tag(BaseTag):
    pass


class StringMixin:    
    is_string = True
    
    def __repr__(self):
        return self.data
    
    def __str__(self):
        return self.data
    
    def __hash__(self) -> int:
        return hash((self.name, self.data, self.index))


class Comment(StringMixin, BaseTag):
    def __init__(self, data):
        super().__init__('comment', {}, ())
        self.data = data


class NewLine(StringMixin, BaseTag):
    def __init__(self, data='\n'):
        super().__init__('newline', {}, [])
        self.data = data
        

class ElementData(StringMixin, BaseTag):
    def __init__(self, data):
        super().__init__('data', {}, [])
        self.data = data
