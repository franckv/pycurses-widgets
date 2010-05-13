import curses

from base import BaseWidget
from statusbar import StatusBar
from commandbar import CommandBar
from titlebar import TitleBar
from panel import Panel

class Screen(BaseWidget):
    def __init__(self, win):
        self.win = win
        self.parent = None
        self.childs = []

        self.status = StatusBar(self)
        self.title = TitleBar(self)
        self.main = Panel(self)
        self.command = CommandBar(self)

        self.set_colors()

    def set_colors(self):
        self.colors = {
            'default': (0, 'COLOR_WHITE', 'COLOR_BLACK'),
            'title': (1, 'COLOR_YELLOW', 'COLOR_BLUE'),
            'status': (1, 'COLOR_YELLOW', 'COLOR_BLUE'),
            'error': (2, 'COLOR_RED', 'COLOR_BLACK'),
            'highlight': (3, 'COLOR_YELLOW', 'COLOR_BLACK'),
        }

        for color in self.colors.itervalues():
            if color[0] == 0: continue
            curses.init_pair(color[0], getattr(curses, color[1]), getattr(curses, color[2]))

    def redraw(self):
        for child in self.childs: child.redraw()

    def refresh(self):
        for child in self.childs: child.refresh()
        #self.win.refresh()
        curses.doupdate()
