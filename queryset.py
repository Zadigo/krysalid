

class ItemsIterable:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def __iter__(self):
        compiler = self.queryset.compiler
        
        # Use the provided query to only partially
        # resolve the tags to their respective
        # instances
        query = self.queryset.query
        if self.queryset.partial and query is not None:
            result = compiler.compile_query(query)

            if result is None:
                return []
            
            for index, item in enumerate(result):
                category, name, attrs, coordinates = item
                instance = compiler.compile_tag(name, attrs, coordinates, category, index)
                yield instance
        else:
            for index, item in enumerate(compiler.result_iteration()):
                category, name, attrs, coordinates = item
                instance = compiler.compile_tag(name, attrs, coordinates, category, index)
                yield instance
            
            
class QuerySet:
    iterable_class = ItemsIterable
    
    def __init__(self, compiler=None, partial=False):
        self.compiler = compiler
        self.result_cache = None
        # NOTE: Could be a Query class?
        self.query = {}
        # Indicates whether the compiler should
        # resolve all the tags on the page
        # or only a partial section -- this is
        # done for optimization purposes and
        # to prevent having to do repetitive
        # page compilation at each run
        self.partial = partial
    
    def __repr__(self):
        data = list(self)
        return f"<{self.__class__.__name__}{data}>"
    
    def __len__(self):
        self.fetch_all()
        return len(list(self.result_cache))
    
    def __iter__(self):
        self.fetch_all()
        return iter(self.result_cache)
    
    @classmethod
    def clone(cls, compiler, partial=False):
        instance = cls()
        instance.compiler = compiler
        instance.partial = partial
        return instance
    
    def fetch_all(self):
        if self.result_cache is None:
            self.result_cache = self.iterable_class(self)
        