import curses
import logging

from .panel import Panel

class TextPanel(Panel):
    def __init__(self, parent):
        super(TextPanel, self).__init__(parent)
        self.lines = []

    def add_line(self, line, style='default'):
        self.lines.append((line, style))
        self.updated = True

    def clear_lines(self):
        self.lines = []
        self.updated = True

    def del_line(self, n):
        if n >= len(self.lines):
            return
        del self.lines[n]

    def refresh(self):
        if self.updated:
            self.win.erase()
            first = True
            (y, x) = self.get_size()
            if y > len(self.lines):
                start = 0
            else:
                start = len(self.lines) - y

            count = 0
            for (line, style) in self.lines[start:]:
                if first:
                    first = False
                else:
                    self.move(count, 0)

                self.write(line)
                count += 1

        super(TextPanel, self).refresh()
