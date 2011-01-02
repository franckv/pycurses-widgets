import curses
import logging

from .textbox import TextBox

class CommandBar(TextBox):
    def __init__(self, parent):
        super(CommandBar, self).__init__(parent)
        self.style = 'command'

    def read(self, prompt, validator = None):
        self.set_text(prompt)
        cmd = ''
        curses.curs_set(2)
        while True:
            c = self.get_char()

            if c is None:
                continue

            if validator and not validator(c):
                continue
        
            (y, x) = self.get_pos()

            if c == '<KEY_ENTER>' or c == '\n':
                self.set_text('')
                curses.curs_set(0)
                return cmd
            elif c == '<KEY_LEFT>':
                logging.debug('left from %i, %i' % (y, x))
                if x > 1:
                    self.move(y, x-1)
                else:
                    self.move(y, x)
            elif c == '<KEY_RIGHT>':
                if x < len(cmd) + 1:
                    self.move(y, x+1)
                else:
                    self.move(y, x)
            elif c == '<KEY_RESIZE>':
                self.screen.send_event(c)
            else:
                (maxy, maxx) = self.get_size()
                # should be screen size
                if len(cmd) > maxx - 3:
                    self.move(y, x)
                else:
                    cmd += c
                    self.set_text('%s%s' % (prompt, cmd))

