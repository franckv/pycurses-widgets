from base import BaseWidget

class Panel(BaseWidget):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.parent.get_size()
        (p_begy, p_begx) = self.parent.get_beg()

        return (p_maxy - 3, p_maxx, p_begy + 1, p_begx)
