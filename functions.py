class Function:
    def as_query(self, compiler):
        pass
    
    
class Combination:
    def combine(self, obj):
        return self


class Q(Function, Combination):
    def __init__(self, *args, negated=False, **kwargs):
        self.negated = negated
        super().__init__(*args, **kwargs)
        
    def __and__(self, obj):
        if not isinstance(obj, Q):
            raise ValueError('Only Q functions can be coerced')
        return self.combine(obj)
    
    def __or__(self, obj):
        pass


class When(Function):
    def __init__(self, condition, then=None, **kwargs):
        pass


c = Q(div__eq='something')
d = c & Q(div__contains='another')
e = d | Q(div__contains='last')

# w = When(tag__eq='div', then='', attrs={'id': 'id'})
