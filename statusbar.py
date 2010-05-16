from ui.ncurses.widget.textbox import TextBox

class StatusBar(TextBox):
    def __init__(self, parent):
        super(StatusBar, self).__init__(parent, -2)
        self.style = 'status'
        self.fill = True

