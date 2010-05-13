# -*- coding: utf-8 -*-   

import curses
import locale

import common
import log

locale.setlocale(locale.LC_ALL, '')

class BaseWidget(object):
    def __init__(self, parent):
        log.debug('%s.init' % self.__class__.__name__)

        self.parent = parent
        self.screen = parent.screen
        self.parent.add_child(self)
        self.childs = []
        (maxy, maxx, posy, posx) = self.get_dimensions()
        self.win = curses.newwin(maxy, maxx, posy, posx)
        #self.win = self.screen.win.subwin(maxy, maxx, posy, posx)
        self.win.keypad(1)
        self.updated = True

    def redraw(self):
        log.debug('%s.redraw' % self.__class__.__name__)

        (maxy, maxx, posy, posx) = self.get_dimensions()
        log.debug((maxy, maxx, posy, posx))
        self.win.resize(maxy, maxx)
        self.win.mvwin(posy, posx)
        for child in self.childs: child.redraw()
        self.updated = True

    def refresh(self):
        log.debug('%s.refresh' % self.__class__.__name__)
        if self.updated:
            log.debug('updated')
            self.win.noutrefresh()
            self.updated = False
        for child in self.childs: child.refresh()
      
    def destroy(self):
        log.debug('%sdestroy' % self.__class__.__name__)
        if self.win: del self.win

    def add_child(self, child):
        self.childs.append(child)

    def get_pos(self):
        return self.win.getyx()

    def get_size(self):
        return self.win.getmaxyx()

    def move(self, y, x):
        log.debug('%s.move %i, %i' % (self.__class__.__name__, y, x))
        self.win.move(y, x)
 
    def write(self, s, attr = None):
        log.debug('%s.write %s', self.__class__.__name__, s)
        if attr is None: attr = curses.A_NORMAL
        self.win.addstr(s.encode(self.parent.encoding), attr)
        self.updated = True

    def get_char(self):
        log.debug('%s.get_char' % self.__class__.__name__)
        result = ''
        count = 0

        self.screen.refresh()
        while True:
            ch = self.win.getch()
            log.debug('ch=%i' % ch)
            if ch == -1:
                return None
            if ch > 255:
                for attr in dir(curses):
                    if attr.startswith('KEY_') and getattr(curses, attr) == ch:
                        return '<%s>' % attr
                return '<%i>' % ch
            result += chr(ch)
            try:
                return result.decode(self.parent.encoding)
            except UnicodeDecodeError as e:
                count += 1
                # assumes multibytes characters are less that 4 bytes
                if count > 4 or e.reason != 'unexpected end of data':
                    return '?'

    def fill(self, c):
        y, x = self.win.getmaxyx()
        s = c * (x - 1)
        for l in range(y):
            self.win.addstr(l, 0, s)

        self.updated = True

