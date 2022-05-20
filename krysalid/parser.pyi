from functools import cached_property
from html.parser import HTMLParser
from typing import Literal, Optional, Type

from krysalid.compiler import Compiler
from krysalid.managers import Manager


class Algorithm(HTMLParser):    
    def __init__(self, **kwargs) -> None: ...


class HTMLPageParser:
    algorithm_class: Type[Algorithm] = ...
    algorithm: Algorithm = ...
    cached_page: str = Literal['']
    compiler: Compiler = ...
    compiler_class: Type[Compiler] = ...
    encoding: str = ...
    objects: Manager = ...

    def __init__(self, html: str = Optional[None], encoding: str = Optional[Literal['utf-8']], **kwargs): ...
    def __repr__(self) -> str: ...    
    @property
    def has_content(self) -> bool: ...    
    @cached_property
    def get_result_cache(self) -> list: ...    
    @classmethod
    def from_file(cls, path: str, encoding: str = Optional[Literal['utf-8']]) -> HTMLPageParser: ...
    def parse_page(self) -> None: ...
