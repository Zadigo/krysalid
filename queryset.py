from itertools import chain

class ItemsIterable:
    """Container that allows optimized iteration
    over a queryset"""
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
            
        for index, items in enumerate(result):
            # category, name, attrs, coordinates = item
            # instance = compiler.compile_tag(name, attrs, coordinates, category, index)
            instance = compiler.compile_tag(items, index)

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
    
    def fetch_all(self):
        """Load the result cache with the
        raw parsed data"""            
        if self.result_cache is None:
            self.result_cache = self.iterable_class(self)
    
    # ######################################
    # Queryset methods are run on the tag  #
    # instances directly and not on the    #
    # raw values                           #
    # #################################### #
        
    def first(self):
        pass
    
    def last(self):
        pass
            
    def count(self):
        pass
            
    def filter(self, *args, **kwargs):
        pass
    
    def find(self, name=None, attrs={}):
        indexes = []
        self.fetch_all()
        for i, tag in enumerate(self.result_cache):
            if 'ST' in tag and name in tag:
                indexes.append(i)
                continue
            
            if 'ET' in tag and name in tag:
                indexes.append(i)
                break

        return indexes
        # return self.result_cache[indexes[0]:indexes[1] + 1]
            
                        
    def find_all(self, name=None, attrs={}):
        indexes = []
        index = []
        self.fetch_all()
        for i, tag in enumerate(self.result_cache):
            if tag.is_opening_tag and name in tag:
                index.append(i)
                continue
            
            if tag.is_closing_tag and name in tag:
                index.append(i)
                indexes.append(index)
                index = []
                continue
        return indexes
        # for i, tag in enumerate(self.result_cache):
        #     if 'ST' in tag and name in tag:
        #         index.append(i)
        #         continue
            
        #     if 'ET' in tag and name in tag:
        #         index.append(i)
        #         indexes.append(index)
        #         index = []
        #         continue
            
        # print(indexes)
        # # TODO: Put abiliy o store chain, iterators or generators
        # # on the queryset so that can be resolved directly
        # result = chain(*list(map(lambda x: self.result_cache[x[0]:x[1] + 1], indexes)))
        # return RawQueryset.clone(self.compiler, result)
        # # queryset = self.clone(self.compiler)
        # # queryset.result_cache = result
        # # return queryset
        
    def get_text(self, seperator=None, clean=True):
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
        """Determines if thee queryset
        has elements"""
        return len(self) > 0
    
    def contains(self, name):
        pass
    
    def explain(self):
        pass
    
    def update_attribute(self, name, attr, value):
        pass


class RawQueryset(QuerySet):
    def __init__(self, compiler, raw_data):
        super().__init__(compiler=compiler)
        self.raw_data = raw_data
        
    @classmethod
    def clone(cls, compiler, data):
        return cls(compiler, data)
    
    def fetch_all(self):
        if self.result_cache is None:
            self.result_cache = self.iterable_class(self, raw_data=self.raw_data)

