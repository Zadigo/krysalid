from krysalid.parsers import Algorithm

class TestExtractor:
    """Blank extractor for testing how the
    algorithm interracts with the extractor"""
    
    def start_tag(self, tag, attrs, **kwargs):
        pass

    def end_tag(self, tag, **kwargs):
        pass

    def internal_data(self, data, **kwargs):
        pass

    def self_closing_tag(self, tag, attrs, **kwargs):
        pass

    def parse_comment(self, data, **kwargs):
        pass


with open('tests/html/test1.html', mode='r', encoding='utf-8') as f:
    a = Algorithm(TestExtractor())
    a.feed(f.read())
    a.close()
