import locale
import curses

import log
from base import BaseWidget

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
                padded_text += u' ' * (x - len(self.text) - 1)
            self.write(padded_text, self.screen.get_color(self.style))

        super(TextBox, self).refresh()

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.parent.get_size()
        (p_posy, p_posx) = self.parent.get_pos()

        if self.relpos >= 0:
            posy = p_posy + self.relpos
        else:
            posy = p_posy + p_maxy + self.relpos

        posx = p_posx

        maxy = 1
        maxx = p_maxx

        return (maxy, maxx, posy, posx)

    def set_text(self, text):
        self.text = text
        self.updated = True
