from base import BaseWidget

class Panel(BaseWidget):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.parent.win.getmaxyx()
        (p_posy, p_posx) = self.parent.win.getyx()

        return (p_maxy - 3, p_maxx, p_posy + 1, p_posx)

    def refresh(self):
        if self.updated:
            self.fill('#')

        super(Panel, self).refresh()
