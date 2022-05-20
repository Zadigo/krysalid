from typing import Generator
from krysalid.queryset import QuerySet

class BaseExtractor:
    def __init__(self, page_parser, skip_newlines=False, *args, **kwargs):
        self.page_parser = page_parser
        self.compiler = page_parser.compiler
        self.skip_newlines = skip_newlines

    def __len__(self):
        return self.get_queryset()
    
    def __repr__(self):
        queryset = self.get_queryset()
        if isinstance(queryset, Generator):
            queryset = list(queryset)
        return str(queryset)
    
    def __iter__(self):
        return iter(self.get_queryset())
    
    def get_queryset(self):
        return []
        

class ImageExtractor(BaseExtractor):
    def get_queryset(self):
        queryset = QuerySet.clone(self.compiler)
        for item in queryset:
            if item == 'img':
                yield item


class TextExtractor(BaseExtractor):
    def get_queryset(self):
        queryset = QuerySet.clone(self.compiler)
        for item in queryset:
            if self.skip_newlines:
                if item == '\n':
                    continue
                
            if item.is_string:
                yield item
                

class TableExtractor(BaseExtractor):
    def get_queryset(self):
        queryset = QuerySet.clone(self.compiler, partial=True)
        queryset.query = {'tag': 'table'}
        return queryset
