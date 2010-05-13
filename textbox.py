import locale

import log
from base import BaseWidget

locale.setlocale(locale.LC_ALL, '')

class TextBox(BaseWidget):
    def __init__(self, parent, relpos):
        self.relpos = relpos
        self.text = ''

        super(TextBox, self).__init__(parent)

    def refresh(self):
        log.debug('refresh %s' % self.__class__.__name__)
        if self.updated:
            self.win.erase()
            self.write(self.text)

        super(TextBox, self).refresh()

    def get_dimensions(self):
        (p_maxy, p_maxx) = self.parent.win.getmaxyx()
        (p_posy, p_posx) = self.parent.win.getyx()

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

    def pad_string(self, s):
        (maxy, maxx) = self.win.getmaxyx()
        #return s + ' ' * (maxx - len(s) - 1)
        return s.ljust(maxx - 1)

    def get_color(self, type):
        if type in self.colors:
            return curses.color_pair(self.colors[type][0])
        else:
            return curses.color_pair(0)

    #def set_title(self, s):
    #    self.title = s
    #    self.win['title'].move(0, 0)
    #    self.win['title'].addstr(s.encode(self.encoding), self.get_color('title') | curses.A_BOLD)
    #    self.win['title'].clrtoeol()
    #    #(y, x) = self.win.getyx()
    #    #self.win.move(0, 0)
    #    #self.write_str(self.pad_string(s), self.get_color('title') | curses.A_BOLD)
    #    #self.win.move(y, x)

    #def set_status(self, s):
    #    self.status = s
    #    self.win['status'].move(0, 0)
    #    self.win['status'].addstr(s.encode(self.encoding), self.get_color('status') | curses.A_BOLD)
    #    #(y, x) = self.win.getyx()
    #    #(maxy, maxx) = self.win.getmaxyx()
    #    #if maxy < 2: return
    #    #self.win.move(maxy-2, 0)
    #    #self.write_str(self.pad_string(s), self.get_color('status') | curses.A_BOLD)
    #    #self.win.move(y, x)

