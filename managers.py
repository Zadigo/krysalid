import itertools

from queryset import QuerySet
from utils import compare_attributes


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
        return self.compiler.get_tag('head')

    @property
    def body(self):
        return self.compiler.body

    def filter(self, *args, **kwargs):
        pass

    def find(self, name=None, attrs={}):
        """Finds the first matching element on
        the page"""
        data = []

        # 1. When there is only the name,
        # return the first matching tag
        # 2. When both name and attrs, get
        # all matching elements with attrs
        # then get the first matching item
        # with the name
        # 3. When only attrs, collect all
        # items and return just the first
        # matching element

        if name is not None and not attrs:
            data = self.compiler.get_tag(name)
            return data

        has_matched = False
        if name is not None and attrs:
            limits = self.compiler.map_indexes_by_attributes(attrs)

            for limit in limits:
                lh, rh = limit
                tag = self.compiler.result_iteration()[lh:rh]

                opening_element = tag[0]
                if name in tag[0] and 'ST' in tag[0]:
                    has_matched = True
                    break
            data = tag if has_matched else []

        if name is None and attrs:
            limits = self.compiler.map_indexes_by_attributes(attrs)

            for limit in limits:
                lh, rh = limit
                tag = self.compiler.result_iteration()[lh:rh]

                opening_element = tag[0]
                result = compare_attributes(opening_element[2], attrs)

                if result:
                    has_matched = True
                    break

            data = tag if has_matched else []
        return data

        # instance = HTMLElement(data)
        # instance.compiler = self.compiler
        # return instance

    def find_all(self, name, attrs={}):
        queryset = QuerySet.clone(self.compiler)
        queryset.query = {'tag': name, 'attrs': attrs}
        return queryset
