from panel import Panel

class TextPanel(Panel):
    def __init__(self, parent):
        super(TextPanel, self).__init__(parent)
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)
        self.updated = True

    def refresh(self):
        if self.updated:
            self.win.erase()
            first = True
            (y, x) = self.get_size()
            if y > len(self.lines):
                start = 0
            else:
                start = len(self.lines) - y

            for line in self.lines[start:]:
                if first:
                    first = False
                else:
                    self.write('\n')
                self.write(line)

        super(TextPanel, self).refresh()
