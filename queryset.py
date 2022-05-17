import inspect


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
    
    def __getitem__(self):
        pass
    
    def __eq__(self, obj):
        pass
    
    def __and__(self, obj):
        pass
    
    def __bool__(self):
        pass
    
    @classmethod
    def clone(cls, compiler, partial=False):
        instance = cls()
        instance.compiler = compiler
        instance.partial = partial
        return instance
    
    # ######################################
    # Queryset methods are run on the tag  #
    # instances directly and not on the    #
    # raw values                           #
    # #################################### #
        
    @property
    def first(self):
        pass
    
    @property
    def last(self):
        pass

    def fetch_all(self):
        """Load the result cache with the
        raw parsed data"""
        if self.result_cache is None:
            self.result_cache = self.iterable_class(self)
            
    def count(self):
        pass
            
    def filter(self, *args, **kwargs):
        pass
    
    def find(self, name, attrs={}):
        pass
        
    def find_all(self, name, attrs={}):
        pass
    
    def distinct(self):
        pass
    
    def exclude(self, tag, attrs={}):
        pass

    def union(self, *querysets):
        pass
    
    def exists(self):
        pass
    
    def contains(self):
        pass
    
    def explain(self):
        pass
    
    def update_attribute(self, name, attr, value):
        pass
