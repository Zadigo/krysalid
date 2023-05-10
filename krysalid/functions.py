from datetime import datetime


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
    
    
# class Expression:
#     def to_python(self, value):
#         pass


# class Date(Expression):
#     format = 'date'
    
#     def __init__(self, tag, attrs={}):
#         pass
    
#     def to_python(self, value):
#         result = datetime.strptime('', value)
#         return result[self.format]


# class TruncYear(Date):
#     format = 'year'
    
        
# class TruncMonth(Date):
#     format = 'month'


# class TruncDay(Date):
#     format = 'day'


# TruncDay()


c = Q(div__eq='something')
d = c & Q(div__contains='another')
e = d | Q(div__contains='last')

# w = When(tag__eq='div', then='', attrs={'id': 'id'})
