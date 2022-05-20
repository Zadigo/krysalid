from email.generator import Generator
from functools import lru_cache
from typing import List, Literal, OrderedDict, Tuple, Type, Union

from krysalid.html_tags import ElementData, Tag
from krysalid.parser import HTMLPageParser


class BaseCompiler:
    clean_page: str = ...
    page_parser: HTMLPageParser = ...
    def __init__(self, page_parser: HTMLPageParser): ...
    def clone(self) -> Compiler: ...
    def map_indexes_by_attributes(self, attrs: dict) -> List[List[int]]: ...
    def map_indexes_by_tag_name(self, name: str) -> List[List[int]]: ...
    def get_top_lower_indexes(self, name: str) -> List[List[int]]: ...
    def get_top_lower_index(self, name: str) -> Tuple[int, int]: ...
    def compile_tag(self, name: str, attrs: dict, coordinates: list[int, int], category: str, index: int) -> Union[Tag, ElementData]: ...
    def detect_category(self, category: str) -> Union[Type[Tag], Type[ElementData]]: ...
    def format_page(self, page: str) -> str: ...
    def pre_compile_setup(self, page: str) -> None: ...
    def result_iteration(self) -> list[Tuple[str, str, list, list]]: ...


class Compiler(BaseCompiler):
    def compile_query(self, query: dict) -> list: ...
    def get_tag(self, name: str) -> list: ...
    def get_tags(self, name: str) -> Generator: ...
    def get_data(self) -> list: ...
    def get_data(self, newlines = Literal[True]) -> list: ...
