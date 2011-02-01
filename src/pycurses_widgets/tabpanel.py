import logging

from . import base
from .panel import Panel

class TabPanel(Panel):
    def __init__(self, parent):
        super(TabPanel, self).__init__(parent)

        self.tabs = {}
        self.layout = base.LAYOUT_OVERLAP
        self.current = None

    def create_tab(self, cls, name):
        if name in self.tabs: return None
        tab = cls(self)
        self.tabs[name] = tab
        tab.name = name

        if not self.current:
            self.current = tab

        return tab

    def delete_tab(self, name = None):
        tab = None
        if name is None and self.current:
            tab = self.current
            name = self.current.name
        elif name is not None and name in self.tabs:
            tab = self.tabs[name]
        
        if tab:
            self.show_next_tab()
            del self.tabs[name]
            self.childs.remove(tab)
            if len(self.childs) == 0:
                self.current = None

    def show_tab(self, name):
        if name in self.tabs:
            self.current = self.tabs[name]
            self.current.updated = True

    def show_next_tab(self):
        if len(self.childs) <= 1:
            return

        idx = self.childs.index(self.current)
        if idx + 1 < len(self.childs):
            logging.debug('Current tab is %i' % (idx + 1))
            next_tab = self.childs[idx + 1]
        else:
            logging.debug('Current tab is %i' % 0)
            next_tab = self.childs[0]
            
        self.current = next_tab
        self.current.updated = True

    def show_prev_tab(self):
        if len(self.childs) <= 1:
            return

        idx = self.childs.index(self.current)
        if idx > 0:
            logging.debug('Current tab is %i' % (idx - 1))
            prev_tab = self.childs[idx - 1]
        else:
            logging.debug('Current tab is %i' % len(self.childs))
            prev_tab = self.childs[-1]
            
        self.current = prev_tab
        self.current.updated = True

    def send_event(self, event):
        return super(TabPanel, self).send_event(event) or (self.current and self.current.send_event(event))

    def refresh(self):
        logging.debug('%s.refresh' % self.__class__.__name__)
        if self.current:
            self.current.refresh()

