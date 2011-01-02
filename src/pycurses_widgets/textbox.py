import locale
import curses
import logging

from .base import *

locale.setlocale(locale.LC_ALL, '')

class TextBox(BaseWidget):
    def __init__(self, parent):
        self.style = 'default'
        self.fill = False
        self.text = ''
        super(TextBox, self).__init__(parent, SIZE_EXTEND, 1)

    def refresh(self):
        logging.debug('%s.refresh' % self.__class__.__name__)
        if self.updated:
            self.win.erase()
            padded_text = self.text
            if self.fill:
                logging.debug('padding: %s' % padded_text)
                (y, x) = self.get_size()
                padded_text += ' ' * (x - len(self.text) - 1)
            (maxy, maxx) = self.get_size()
            if len(padded_text) >= maxx - 1:
                padded_text = padded_text[:maxx-1]
            self.write(padded_text, self.screen.get_color(self.style))

        super(TextBox, self).refresh()

    def set_text(self, text):
        self.text = text
        self.updated = True
