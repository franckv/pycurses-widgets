import logging
import curses

from pycurses_widgets import Screen, StatusBar, CommandBar, TitleBar, TextPanel, TabPanel

class Window(Screen):
    def __init__(self, win):
        super(Window, self).__init__(win)

        self.title = TitleBar(self)

        self.main = TabPanel(self)
        self.main.create_tab(TextPanel, 'main')
        self.main.create_tab(TextPanel, 'help')
        self.main.tabs['help'].add_line('Help !')

        self.status = StatusBar(self)
        self.command = CommandBar(self)

        self.register_event('<KEY_TAB>', self.show_next_tab)
        self.register_event('<KEY_BTAB>', self.show_prev_tab)

        self.redraw()

    def set_title(self, text):
        self.title.set_text(text)

    def set_status(self, text):
        self.status.set_text(text)

    def show_next_tab(self):
        self.main.show_next_tab()
        self.update_title()

    def show_prev_tab(self):
        self.main.show_prev_tab()
        self.update_title()

    def update_title(self):
        title = ''
        for tab in self.main.childs:
            if title != '':
                title += ' '
            if tab.name == self.main.current.name:
                title += '[%s]' % tab.name
            else:
                title += tab.name

        self.set_title('%s v%s %s' % (common.PROGNAME, common.PROGVERSION, title))

    def run(self):
        curses.curs_set(0)
        while True:
            c = self.command.get_char()
            if c == 'q':
                break


def main(stdscr):
    screen = Window(stdscr)

    screen.set_title('%s v%s' % ("TEST", "0.1"))
    screen.set_status('Standby ready')

    screen.refresh()

    screen.run()

def run(args = None):
    curses.wrapper(main)

if __name__ == "__main__":
    logging.basicConfig(
        level = logging.DEBUG,
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename = '/tmp/widget.log',
        filemode = 'w'
    )

    run()

