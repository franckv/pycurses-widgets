import curses

import log
from base import BaseWidget
from textpanel import TextPanel

class ItemList(TextPanel):
    def __init__(self, parent):
        super(ItemList, self).__init__(parent)
        self.selected = None

    def move_up(self):
        log.debug('moving up')
        if len(self.lines) == 0:
            return
        elif self.selected is None:
            self.selected = 0
            self.updated = True
        elif self.selected > 0:
            self.selected -= 1
            self.updated = True

        log.debug('selected is %i' % self.selected)

    def move_down(self):
        log.debug('moving down')
        if len(self.lines) == 0:
            return
        elif self.selected is None:
            self.selected = 0
            self.updated = True
        elif self.selected < len(self.lines) - 1:
            self.selected += 1
            self.updated = True

        log.debug('selected is %i' % self.selected)

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
            for line in self.lines[start:]:
                if first:
                    first = False
                else:
                    self.move(count, 0)

                if self.selected == count + start:
                    padded = line + u' ' * (x - len(line) - 1)
                    self.write(padded, self.screen.get_color('highlight'))
                else:
                    self.write(line)
                count += 1
            
            BaseWidget.refresh(self)

