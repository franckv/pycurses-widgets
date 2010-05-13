# -*- coding: utf-8 -*-   

import curses
import locale

import common

locale.setlocale(locale.LC_ALL, '')

class BaseWidget(object):
    def __init__(self, parent, maxy, maxx, posy, posx):
        self.parent = parent
        self.parent.add_child(self)
        self.childs = []
        self.win = curses.newwin(maxy, maxx, posy, posx)

    def redraw(self, maxy, maxx, posy, posx):
        #if self.win: del self.win
        #self.win = curses.newwin(maxy, maxx, posy, posx)
        self.win.resize(maxy, maxx)
        self.win.mvwin(posy, posx)
        for child in self.childs: child.redraw()
        
    def add_child(self, child):
        self.childs.append(child)

    def get_pos(self):
        return self.win.getyx()

    def get_size(self):
        return self.win.getmaxyx()

    def move(self, y, x):
        self.win.move(y, x)
 
    def write(self, s, attr = None):
        if attr is None: attr = curses.A_NORMAL
        (y, x) = self.win.getyx()
        self.win.addstr(s.encode(self.parent.encoding), attr)

    def get_char(self):
        result = ''
        count = 0

        self.parent.refresh()
        while True:
            ch = self.win.getch()
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

    def resize(self):
        self.redraw()
        self.refresh()

    def clear(self):
        self.win.clear()

    def refresh(self):
        #self.win.refresh()
        self.win.noutrefresh()
        for child in self.childs: child.refresh()

