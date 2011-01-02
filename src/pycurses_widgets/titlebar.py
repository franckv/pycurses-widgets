from .textbox import TextBox

class TitleBar(TextBox):
    def __init__(self, parent):
        super(TitleBar, self).__init__(parent)
        self.style = 'title'
        self.fill = True

