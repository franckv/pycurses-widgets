from ui.ncurses.widget.base import BaseWidget

class Panel(BaseWidget):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.screen.get_size()
        (p_begy, p_begx) = self.screen.get_beg()

        # TODO : hardcoded
        return (p_maxy - 3, p_maxx, p_begy + 1, p_begx)
