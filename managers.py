from krysalid.queryset import QuerySet

class Manager:
    def __init__(self):
        self.compiler = None
        self.name = 'objects'
        
    def __repr__(self):
        return f"<{self.__class__.__name__}[for={self.name}]>"
        
    def __get__(self, instance, cls=None):
        self.compiler = instance.compiler
        return self
    
    @property
    def html(self):
        pass
    
    @property   
    def head(self):
        pass

    @property
    def body(self):
        pass
    
    def filter(self, *args, **kwargs):
        pass
    
    def find(self, tag, attrs=None):
        if attrs is None:
            # NOTE: Return the first occurance of
            # a tag if the user does not provide
            # any other defining attributes
            queryset = QuerySet.clone(self.compiler, partial=True)
            queryset.query = {'tag': tag, 'attrs': attrs}
            return queryset
    
    def find_all(self, tag, attrs=None):
        pass
