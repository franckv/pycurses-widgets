import curses
import logging

from .base import BaseWidget
from .textpanel import TextPanel

class ItemList(TextPanel):
    def __init__(self, parent):
        super(ItemList, self).__init__(parent)
        self.selected = None
        self.on_selected = None
        self.register_event('<KEY_UP>', self.move_up)
        self.register_event('<KEY_DOWN>', self.move_down)
        self.register_event('<KEY_ENTER>', self.item_selected)
        self.register_event('<KEY_SPACE>', self.item_selected)

    def move_up(self, event):
        logging.debug('moving up')
        if len(self.lines) == 0:
            return
        elif self.selected is None:
            self.selected = 0
            self.updated = True
        elif self.selected > 0:
            self.selected -= 1
            self.updated = True

        logging.debug('selected is %i' % self.selected)

    def move_down(self, event):
        logging.debug('moving down')
        if len(self.lines) == 0:
            return
        elif self.selected is None:
            self.selected = 0
            self.updated = True
        elif self.selected < len(self.lines) - 1:
            self.selected += 1
            self.updated = True

        logging.debug('selected is %i' % self.selected)

    def set_selected(self, cb):
        self.on_selected = cb

    def item_selected(self, event):
        if not self.selected is None:
            logging.debug('enter pressed on item %i' % self.selected)
            if self.on_selected:
                self.on_selected(self.selected)

    def refresh(self):
        if self.updated:
            self.win.erase()
            first = True
            (y, x) = self.get_size()
            if y > len(self.lines):
                start = 0
            else:
                # TODO: selected item should be in the range
                start = len(self.lines) - y

            count = 0
            for (line, style) in self.lines[start:]:
                if first:
                    first = False
                else:
                    self.move(count, 0)

                if self.selected == count + start:
                    padded = line + ' ' * (x - len(line) - 1)
                    self.write(padded, self.screen.get_color('highlight'))
                else:
                    self.write(line)
                count += 1
            
            BaseWidget.refresh(self)

