from textbox import TextBox

class CommandBar(TextBox):
    def __init__(self, parent):
        super(CommandBar, self).__init__(parent, -1)

    def read(self):
        (maxy, maxx) = self.win.getmaxyx()
        (posy, posx) = self.win.getyx()
        if maxy < 1: return
        self.win.move(maxy-1, 0)

        self.write_str(':')
        cmd = ''

        count = 0
        while(True):
            count += 1
            c = self.get_char()
            if c is None:
                continue
            elif c == '<KEY_ENTER>' or c == '\n':
                break
            elif c == '<KEY_LEFT>':
                (y, x) = self.win.getyx()
                self.move(y, x-1)
            elif c == '<KEY_RIGHT>':
                (y, x) = self.win.getyx()
                self.move(y, x+1)
            else:
                # should be screen size
                if len(cmd) >= maxx - 2:
                    continue
                cmd += c
                self.write_str(c)
                self.set_status('%i/%i <%s> %i' % (len(cmd), maxx, c.strip(), count))

        self.handle_command(cmd)

        self.clear_line()
        self.move(posy, posx)

    def handle_command(self, cmd):
        if cmd == 'q' or cmd == 'quit':
            sys.exit(0)


