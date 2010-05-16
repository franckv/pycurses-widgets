import sys
import curses
import locale

import log
import config
from ui.ncurses.widget.base import BaseWidget

locale.setlocale(locale.LC_ALL, '')

class Screen(BaseWidget):
    def __init__(self, win):
        super(Screen, self).__init__(None, win)
        self.encoding = locale.getpreferredencoding()

        # TODO: make it generic
        self.set_colors()

        self.register_event('<KEY_RESIZE>', self.redraw)

    def set_colors(self):
        curses.use_default_colors()
        for color in config.colors.itervalues():
            if color[0] == 0: continue
            curses.init_pair(
                color[0],
                getattr(curses, 'COLOR_' + color[1]),
                getattr(curses, 'COLOR_' + color[2])
            )

    def get_colors(self):
        return self.colors

    def get_color(self, type):
        if not type in config.colors:
            type = 'default'
        return curses.color_pair(
                config.colors[type][0]) | getattr(curses, 'A_' + config.colors[type][3])

    def redraw(self):
        log.debug('redraw')
        for child in self.childs: child.redraw()

    def refresh(self):
        log.debug('refresh')
        for child in self.childs:
            log.debug('child %s' % child.__class__.__name__)
            child.refresh()
        curses.doupdate()

    def destroy(self):
        for child in self.childs: child.destroy()
        sys.exit(0)
