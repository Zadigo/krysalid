class ItemsIterable:
    def __init__(self, queryset, raw_data=[]):
        self.queryset = queryset
        self.raw_data = raw_data
    
    def __iter__(self):
        compiler = self.queryset.compiler
        query = self.queryset.query
        
        if compiler is None:
            raise ValueError(f"{self.__class__.__name__} requires a compiler in order to transform elements "
                             "to their corresponsding Python representation")
        
        uses_query = False
        if query:
            uses_query = True
            result = compiler.compile_query(query)
        elif self.raw_data:
            # In certain cases, the queryset wants
            # to resolve data not coming from the
            # compiler directly but from a partial
            # set of items
            result = self.raw_data
        else:
            result = compiler.result_iteration()
            
        for index, item in enumerate(result):
            category, name, attrs, coordinates = item
            instance = compiler.compile_tag(name, attrs, coordinates, category, index)
            if uses_query:
                # Integrate the raw instance values
                # to the instance in order for it
                # to be able to compute it's children tags
                pass
            yield instance
            
            
class QuerySet:
    iterable_class = ItemsIterable
    
    def __init__(self, compiler=None):
        self.compiler = compiler
        self.result_cache = None
        # NOTE: Could be a Query class?
        self.query = {}
    
    def __repr__(self):
        data = list(self)
        return f"<{self.__class__.__name__}{data}>"
    
    def __len__(self):
        self.fetch_all()
        return len(list(self.result_cache))
    
    def __iter__(self):
        self.fetch_all()
        return iter(self.result_cache)
    
    def __getitem__(self, index):
        pass
    
    def __eq__(self, obj):
        pass
    
    def __and__(self, obj):
        pass
    
    def __or__(self, obj):
        pass
    
    def __bool__(self):
        pass
    
    @classmethod
    def clone(cls, compiler):
        return cls(compiler=compiler)
    
    # ######################################
    # Queryset methods are run on the tag  #
    # instances directly and not on the    #
    # raw values                           #
    # #################################### #
        
    def first(self):
        pass
    
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
    
    def difference(self, *queryets):
        pass
    
    def exists(self):
        pass
    
    def contains(self):
        pass
    
    def explain(self):
        pass
    
    def update_attribute(self, name, attr, value):
        pass


class RawQueryset(QuerySet):
    def __init__(self, compiler, raw_data):
        super().__init__(compiler=compiler)
        self.raw_data =raw_data
        
    @classmethod
    def clone(cls, compiler, data):
        return cls(compiler, data)
    
    def fetch_all(self):
        if self.result_cache is None:
            self.result_cache = self.iterable_class(self, raw_data=self.raw_data)

