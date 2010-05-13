from base import BaseWidget

class Panel(BaseWidget):
    def __init__(self, parent):
        (p_maxy, p_maxx) = parent.win.getmaxyx()
        (p_posy, p_posx) = parent.win.getyx()

        super(Panel, self).__init__(parent, p_maxy - 3, p_maxx, p_posy + 1, p_posx)
        self.fill('#')

    def redraw(self):
        (p_maxy, p_maxx) = self.parent.win.getmaxyx()
        (p_posy, p_posx) = self.parent.win.getyx()

        super(Panel, self).redraw(p_maxy - 3, p_maxx, p_posy + 1, p_posx)
        self.fill('#')
