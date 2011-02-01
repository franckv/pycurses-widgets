# -*- coding: utf-8 -*-   

import curses
import locale
import logging

from . import chars

locale.setlocale(locale.LC_ALL, '')

LAYOUT_VERTICAL, LAYOUT_HORIZONTAL, LAYOUT_OVERLAP = list(range(3))
SIZE_EXTEND, SIZE_SHRINK = (-1, -2)

class BaseWidget(object):
    def __init__(self, parent, width, height, win = None):
        logging.debug('%s.init' % self.__class__.__name__)

        self.width = width
        self.height = height

        self.parent = parent
        if parent is None:
            self.screen = self
        else:
            self.screen = parent.screen
            self.parent.add_child(self)

        if win:
            self.win = win
        else:
            self.win = curses.newwin(0, 0, 0, 0)
            #self.win = curses.newwin(*self.get_dimensions())
            #self.win = self.screen.win.subwin(*self.get_dimensions())
            self.win.keypad(1)
 
        self.layout = LAYOUT_VERTICAL
        self.childs = []
        self.updated = True
        self.events = {}

    def get_child_dimensions(self, child):
        logging.debug('%s.get_child_dimensions' % self.__class__.__name__)
        maxy, maxx = self.get_size()
        begy, begx = self.get_beg()
        logging.debug('maxy: %i, maxx: %i, begy: %i, begx: %i' % (maxy, maxx, begy, begx))

        if self.layout == LAYOUT_OVERLAP:
            dimensions = (maxy, maxx, begy, begx)
        elif self.layout == LAYOUT_VERTICAL or self.layout == LAYOUT_HORIZONTAL:
            fixed = 0   # total size of fixed sized items
            n = 0       # number of dynamic sized items
            for c in self.childs:
                if self.layout == LAYOUT_VERTICAL:
                    dim = c.height
                else:
                    dim = c.width
                if dim == SIZE_EXTEND:
                    n += 1
                else:
                    fixed += dim

            # the space not taken by fixed sized items is divided among the others
            if n > 0:
                if self.layout == LAYOUT_VERTICAL:
                    q, r = (int((maxy-fixed)/n), (maxy-fixed)%n)
                else:
                    q, r = (int((maxx-fixed)/n), (maxx-fixed)%n)
            else:
                q, r = (0, 0)

            logging.debug('Fixed: %i, n: %i, q: %i, r: %i' % (fixed, n, q, r))
            if self.layout == LAYOUT_VERTICAL:
                start = begy
            else:
                start = begx
            for c in self.childs:
                if self.layout == LAYOUT_VERTICAL:
                    dim = c.height
                else:
                    dim = c.width

                if dim == SIZE_EXTEND:
                    dim = q
                    if r > 0:
                        dim += 1
                        r -= 1

                if c == child:
                    if self.layout == LAYOUT_VERTICAL:
                        width = c.width
                        if width == SIZE_EXTEND:
                            width = maxx
                        dimensions = (dim, width, start, begx)
                        break
                    else:
                        height = c.height
                        if height == SIZE_EXTEND:
                            height = maxy
                        dimensions = (height, dim, start, begx)
                        break

                start += dim

        logging.debug('maxy: %i, maxx: %i, begy: %i, begx: %i' % dimensions)
        return dimensions

    def get_dimensions(self):
        logging.debug('%s.get_dimensions' % self.__class__.__name__)
        if self.parent is None:
            maxy, maxx = self.get_size()
            begy, begx = self.get_beg()
            dimensions = (maxy, maxx, begy, begx)
        else:
            dimensions = self.parent.get_child_dimensions(self)

        logging.debug('maxy: %i, maxx: %i, begy: %i, begx: %i' % dimensions)
        return dimensions

    def get_pos(self):
        return self.win.getyx()

    def get_beg(self):
        return self.win.getbegyx()

    def get_size(self):
        return self.win.getmaxyx()

    def redraw(self):
        logging.debug('%s.redraw' % self.__class__.__name__)

        (maxy, maxx, posy, posx) = self.get_dimensions()
        logging.debug((maxy, maxx, posy, posx))
        self.win.resize(maxy, maxx)
        self.win.mvwin(posy, posx)
        for child in self.childs: child.redraw()
        self.updated = True

    def refresh(self):
        logging.debug('%s.refresh' % self.__class__.__name__)
        if self.updated:
            logging.debug('updated')
            self.win.noutrefresh()
            self.updated = False
        for child in self.childs: child.refresh()
      
    def move(self, y, x):
        logging.debug('%s.move %i, %i' % (self.__class__.__name__, y, x))
        self.win.move(y, x)

    def write(self, s, attr = None):
        logging.debug('%s.write %s', self.__class__.__name__, s)
        if attr is None: attr = curses.A_NORMAL
        #self.win.addstr(s.encode(self.screen.encoding), attr)
        self.win.addstr(s, attr)
        self.updated = True
       
    def fill(self, c):
        y, x = self.win.getmaxyx()
        s = c * (x - 1)
        for l in range(y):
            self.win.addstr(l, 0, s)

        self.updated = True

    def destroy(self):
        logging.debug('%sdestroy' % self.__class__.__name__)
        if self.win: del self.win

    def register_event(self, event, method):
        self.events[event] = method

    def send_event(self, event):
        if event in self.events:
            self.events[event](event)
            return True
        logging.debug('Unhandled: %s' % event)
        return False

    def handle_events(self):
        while True:
            c = self.get_char()
            if not c is None:
                logging.debug('Handling event %s' % c)
                self.send_event(c)


    def add_child(self, child):
        self.childs.append(child)
 
    def get_char(self):
        logging.debug('%s.get_char' % self.__class__.__name__)
        result = b""
        count = 0

        self.screen.refresh()
        while True:
            ch = self.win.getch()
            logging.debug('ch=%i' % ch)
            if ch == -1:
                return None
            if ch > 255:
                for attr in dir(curses):
                    if attr.startswith('KEY_') and getattr(curses, attr) == ch:
                        logging.debug('<%s>' % attr)
                        return '<%s>' % attr
                logging.debug('<%i>' % ch)
                return '<%i>' % ch
            result += bytes((ch,))
            logging.debug(result)
            try:
                decoded = result.decode(self.screen.encoding)
                logging.debug('%s: %s (%i)' % (self.screen.encoding, decoded, ord(decoded)))
                # map control characters
                if len(decoded) == 1 and ord(decoded) in chars.mappings:
                    logging.debug('Remap to %s' % chars.mappings[ord(decoded)])
                    return chars.mappings[ord(decoded)]
                else:
                    return decoded
            except UnicodeDecodeError as e:
                count += 1
                logging.debug('Cannot decode')
                # assumes multibytes characters are less that 4 bytes
                if count > 4 or e.reason != 'unexpected end of data':
                    return '?'

