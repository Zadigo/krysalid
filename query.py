class WhereNode:
    def __init__(self, tag, attrs=[]):
        self.decomposed_tag = tag
        self.decomposed_attrs = attrs
    
    def __str__(self):
        return f"<{self.decomposed_tag[-1]} {self.construct_attrs()}>"
    
    def __eq__(self, value):
        name = self.decomposed_tag[-1]
        attrs = [x[-1] == value for x in self.decomposed_attrs]
        return value == name or any(attrs)
    
    def construct_attrs(self):
        base = "[{content}]"
        items = map(lambda x: f"{x[0]}={x[-1]}", self.decomposed_attrs)
        joined_items = ', '.join(items)
        return base.format(content=joined_items)
    
    def compare(self, tag, attrs):
        return self.decomposed_tag == tag and self.decomposed_attrs == attrs
    

class Expression:
    def get_operator(self, name):
        operators = ['eq', 'icontains', 'contains', 'gt', 'gte', 'lt', 'lte']
        if name not in operators:
            raise ValueError()
        return f"__{name}="
    
    def get_tag(self, tag):
        tag = tag.lower()
        return 'tag', self.get_operator('eq'), tag 
    
    def get_attrs(self, attrs):
        values = attrs.items()
        return [(x[0], self.get_operator('eq'), x[1]) for x in values]
        
    def transform_from_string(self, tag, attrs):
        tag = self.get_tag(tag)
        attrs = self.get_attrs(attrs)
        return tag, attrs


class Query(Expression):
    where_node_class = WhereNode
    
    AND = 'AND'
    OR = 'OR'
    
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        decomposed_tag, decomposed_attrs = self.transform_from_string(tag, attrs)
        self.where_node = self.where_node_class(decomposed_tag, decomposed_attrs)
        
        internal_query = []
        tag_query = ''.join(decomposed_tag)
        decomposed_attrs = map(lambda x: ''.join(x), decomposed_attrs)
        internal_query.extend([tag_query])
        internal_query.extend(list(decomposed_attrs))       
        print(internal_query)
        
    def __repr__(self):
        return f"<AND: {self.where_node}>"
    
    # def __eq__(self, value):
    #     return value == self.node
    
    def reconstruct(self):
        return self.tag, list(self.attrs.items())
    
    def compile(self, tag):
        tag, attrs = self.transform_from_string(tag.name, tag.attrs)
        return self.where_node.compare(tag, attrs)
    
    def compile_raw(self, items):
        if not isinstance(items, (list, tuple)):
            raise ValueError()
        items = list(items)
        return self.where_node.compare(items[0], items[1])
        

from krysalid.html_tags import Tag
div = Tag('div', {'id': 'google'}, (1, 1))
q = Query('div', {'id': 'kendall', 'class': 'google'})
# print(q.compile(div))
print(q.compile_raw(('div', [('id', 'Kendall')], (1, 1))))
print(q)
