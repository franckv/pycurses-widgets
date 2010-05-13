import sys
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
        self.screen = self
        self.childs = []

        self.status = StatusBar(self)
        self.title = TitleBar(self)
        self.main = Panel(self)
        self.command = CommandBar(self)

        self.set_colors()

    def set_encoding(self, encoding):
        self.encoding = encoding

    def set_handler(self, handler):
        self.handler = handler

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

    def set_status(self, text):
        self.status.set_text(text)
        self.refresh()

    def redraw(self):
        for child in self.childs: child.redraw()

    def refresh(self):
        for child in self.childs: child.refresh()
        #self.win.refresh()
        #curses.doupdate()

    def destroy(self):
        for child in self.childs: child.destroy()
        sys.exit(0)

    def get_char(self):
        return self.command.get_char()

    def read_command(self):
        return self.command.read()
