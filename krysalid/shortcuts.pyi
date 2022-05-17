class BaseExtractor:
    def __init__(self, *args, **kwargs): ...


class ImageExtractor(BaseExtractor): ...


class TextExtractor(BaseExtractor):
    pass


class TableExtractor(BaseExtractor):
    pass
