import locale

from textbox import TextBox

class CommandBar(TextBox):
    def __init__(self, parent):
        super(CommandBar, self).__init__(parent, -1)

    def read(self):
        self.set_text(':')
        cmd = ''
        while True:
            c = self.get_char()

            if c is None:
                continue

            (y, x) = self.get_pos()
            self.screen.set_status('(%i, %i) : <%s>' % (y, x, c.strip()))
        
            if c == '<KEY_ENTER>' or c == '\n':
                self.clear()
                return cmd
            elif c == '<KEY_LEFT>':
                (y, x) = self.win.getyx()
                self.move(y, x-1)
            elif c == '<KEY_RIGHT>':
                (y, x) = self.win.getyx()
                self.move(y, x+1)
            else:
                (maxy, maxx) = self.win.getmaxyx()
                # should be screen size
                if len(cmd) >= maxx - 2:
                    continue
                cmd += c
                self.set_text(':%s' % cmd)

