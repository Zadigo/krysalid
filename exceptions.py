class TagExistsError(Exception):
    def __init__(self, name):
        message = f"Element with tag name '{name}' does not exist"
        super().__init__(message)


class PathNotExistsError(Exception):
    def __init__(self, path):
        super().__init__(path)
