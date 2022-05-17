class Function:
    def as_query(self, compiler):
        pass
    
    
class Combination:
    pass


class Q(Function, Combination):
    def __init__(self, *args, negated=False, **kwargs):
        self.negated = negated
        super().__init__(*args, **kwargs)


class When(Function):
    def __init__(self, condition, then=None, **kwargs):
        pass


c = Q(div__eq='something')
d = c & Q(div__contains='another')
e = d | Q(div__contains='last')

w = When()
