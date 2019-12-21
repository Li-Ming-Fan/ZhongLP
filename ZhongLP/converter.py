

from .converter_pk.langconv import Converter as ConverterOri


class Converter():
    """
    """
    def __init__(self):
        """
        """
        self.converter_t2s = ConverterOri("zh-hans")

    def convert2simplified(self, text):
        """
        """
        return self.converter_t2s.convert(text)
        #
