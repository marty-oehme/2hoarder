class Wallabag_Converter:
    def __init__(self, data: list[object]):
        self.data = data

    def convert(self) -> object:
        raise NotImplementedError()
