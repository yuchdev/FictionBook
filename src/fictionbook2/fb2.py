# -*- coding: utf-8 -*-
from fictionbook2.writer import Fb2Writer
from fictionbook2.reader import Fb2Reader


class FictionBook2(Fb2Reader, Fb2Writer):
    """
    FictionBook2 class provides methods to deserialize and serialize FB2 books
    """
    def __init__(self, file_path, images_dir):
        """
        Init both bases
        :param file_path: 
        :param images_dir: 
        """
        Fb2Reader.__init__(self, file_path, images_dir)
        Fb2Writer.__init__(self)
