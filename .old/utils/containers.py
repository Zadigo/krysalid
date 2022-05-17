import itertools

class BaseIterable:
    def __init__(self, items, chunk_size=100):
        self.items = items
        self.chunk_size = chunk_size


class TagsIterable(BaseIterable):
    """A iterator that yields tags by chunks for
    optimization purposes"""

    def __iter__(self):
        iterator = iter(self.items)
        while True:
            chunk = tuple(itertools.islice(iterator, self.chunk_size))
            if not chunk:
                break
            yield chunk
