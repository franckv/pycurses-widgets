import locale
import curses

import log
from ui.ncurses.widget.base import BaseWidget

locale.setlocale(locale.LC_ALL, '')

class TextBox(BaseWidget):
    def __init__(self, parent, relpos):
        self.relpos = relpos
        self.style = 'default'
        self.fill = False
        self.text = ''
        super(TextBox, self).__init__(parent)

    def refresh(self):
        log.debug('%s.refresh' % self.__class__.__name__)
        if self.updated:
            self.win.erase()
            padded_text = self.text
            if self.fill:
                log.debug('padding: %s' % padded_text)
                (y, x) = self.get_size()
                padded_text += ' ' * (x - len(self.text) - 1)
            (maxy, maxx) = self.get_size()
            if len(padded_text) >= maxx - 1:
                padded_text = padded_text[:maxx-1]
            self.write(padded_text, self.screen.get_color(self.style))

        super(TextBox, self).refresh()

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.parent.get_size()
        (p_begy, p_begx) = self.parent.get_beg()

        if self.relpos >= 0:
            begy = p_begy + self.relpos
        else:
            begy = p_begy + p_maxy + self.relpos

        begx = p_begx

        maxy = 1
        maxx = p_maxx

        return (maxy, maxx, begy, begx)

    def set_text(self, text):
        self.text = text
        self.updated = True
