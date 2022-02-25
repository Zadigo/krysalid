import itertools
from typing import Generator, Iterator, List, Tuple, Union

from krysalid.utils.iteration import (drop_while, filter_by_name,
                                      filter_by_name_or_attrs)


class BaseQueryset:
    def __init__(self):
        self._data = []

    def __repr__(self):
        return f"<Queryset[{self._data}]>"

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)
    
    def __contains__(self, obj):
        return obj in self._data
    
    def __bool__(self):
        return bool(self._data)
    
    def __and__(self, obj):
        querysets = []
        querysets.extend(self._data)
        querysets.extend(obj._data)
        return self.copy(querysets)
    
    @property
    def last(self):
        return self._data[-1]

    @property
    def count(self):
        return len(self._data)

    @classmethod
    def copy(cls, data: Union[Generator, Iterator]):
        instance = cls()
        # NOTE: Technically the evaluation of
        # a list of items is done as late
        # as possible in order to improve
        # performance. Check how effective
        # this technique is.
        instance._data = list(data)
        return instance

    
class ValuesQueryset(BaseQueryset):
    """Special queryset for lists of attributes
    like ids, classes etc"""
    
    def __init__(self):
        # Keeps track of the relationship between
        # the value and the tag from which
        # said value comes from
        self._relationships = []
        super().__init__()
            
    def find_all(self, value: str):
        """Returns all items from the queryset that matches
        the given value"""
        def results():
            for item in self._data:
                if value in item:
                    yield item
        return self.copy(results())
    
    def flatten(self):
        """A multiple dimension list is flattened
        to a 1D list"""
        return self.copy(itertools.chain(*self._data))
    
    def distinct(self):
        """Keep only unique value"""
        return self.copy(set(self._data))
    
    # def as_tags(self):
    #     """Returns the corresponding tags based on
    #     # TODO: To go from tags to result we have
          # to work directly with the relationships
    #     the result of the previous query"""
    #     return QuerySet.copy((item[0] for item in self._relationships))


class QuerySet(BaseQueryset):
    """Represents the aggregation of multiple
    tags from the html page"""

    @property
    def first(self):
        return self._data[0]
    
    # def save(self, filename: str):
    #     pass

    def find(self, name: str, attrs: dict = {}):
        """Get a tag by name or attribute. If there are multiple
        tags, the first item of the list is returned"""
        result = filter_by_name_or_attrs(self._data, name, attrs)
        return list(result)[0]

    def find_all(self, name: str, attrs: dict = {}):
        """Filter tags by name or by attributes"""
        result = filter_by_name_or_attrs(self._data, name, attrs)
        return QuerySet.copy(result)

    def exclude(self, name: str, attrs: dict={}):
        """Exclude tags with a specific name or attribute"""
        def filtering_function(x):
            return x.name == name and x.attrs == attrs
        result = drop_while(filtering_function, self._data)
        return QuerySet.copy(result)

    # def distinct(self, *attrs):
    #     """Return tags with a distinct attribute"""

    def values(self, *attrs: Tuple[str], include_fields: bool=False):
        """Return the string or an attribute contained 
        for each tag in the queryset. By default, if no
        attribute is provided, the string is returned
        by default"""
        contents = []
        relationships = []
        
        attrs = list(attrs)
        
        if not attrs:
            attrs.append('string')
        
        for item in self._data:
            values = []
            for attr in attrs:
                if attr == 'string':
                    values.append(getattr(item, attr))
                else:
                    values.append(item[attr])
            contents.append(values)
            relationships.append((item, values))
            
        if include_fields:
            contents.insert(0, list(attrs))
        
        queryset = ValuesQueryset.copy(contents)
        queryset._relationships = relationships
        return queryset
    
    # def values_list(self, *attrs):
    #     """Returns a list of tuples using the provided 
    #     attributes e.g. [(('id', 'test'), ('data', 'test'))]
    #     """

    # def dates(self, name: str = None):
    #     """If a tag is a date type e.g. <datetime /> or contains a date, this
    #     will transform the values within them to a list of python
    #     datetime objects"""

    def union(self, *querysets):
        """Combine the results of one or more querysets
        into a new queryset
        
        Example
        -------
        
            q1 = queryset.find_all('a')
            
            q2 = queryset.find_all('html')
            
            q3 = q1.union(q2)
        """
        results = []
        results.extend(self._data)
        for queryset in querysets:
            if not isinstance(queryset, QuerySet):
                raise TypeError('Queryset is not an instance of Queryet')
            results.extend(queryset._data)
        return self.copy(results)

    def exists(self):
        """Checks whether there are any 
        items in th quersyet"""
        return self.count > 0

    def contains(self, name: str):
        """Checks if a tag exists within the queryset"""
        results = []
        for item in self._data:
            results.append(name == item.name)
        return any(results)

    def explain(self):
        """Returns explicit information about the items contained
        in the queryset e.g. link <a> with data ... x attributes"""
        for i, item in enumerate(self._queryset_or_internal_data):
            msg = f"{i}. name: {item.name}, tag: {repr(item)}, children: {len(item.children)}"
            print(msg)

    def generator(self, name: str, attrs: dict = {}):
        """Defers the evaluation of the query to a latter time"""
        return filter_by_name_or_attrs(self._data, name , attrs)

    def update_attr(self, name: str, attr: str, value: str):
        """
        Update the attribute list of a list of items
        within the queryset
        """
        items = list(filter_by_name(self._data, name))
        for item in items:
            item.update_attr(attr, value)
        return QuerySet.copy(items)

    # def filter(self, *funcs):
    #     """Function for running more complexe
    #     queries on the html page"""
    #     pass
