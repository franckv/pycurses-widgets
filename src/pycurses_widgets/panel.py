from .base import *

class Panel(BaseWidget):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, SIZE_EXTEND, SIZE_EXTEND)
