from typing import Optional
from krysalid.compiler import BaseCompiler

class Function:
    def as_query(self, compiler: BaseCompiler): ...
    
    
class Combination:
    pass


class Q(Function, Combination):
    negated: bool = ...
    def __init__(self, *args, negated: Optional[bool] = ..., **kwargs) -> None: ...


class When(Function):
    def __init__(self, condition: str, then: str = ..., **kwargs) -> None: ...
