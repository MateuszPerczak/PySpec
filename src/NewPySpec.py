from tkinter import Tk
from Pages import Settings, Processor, Memory, Storeage, VideoCard
from Components import View
from Components.NavigationView import NavigationView
from Components.Debugger import Debugger
from Components.SysInfo import Provider

class PySpec(Tk):
    def __init__(self: object) -> object:
        super().__init__()
        self.title('PySpec')
        self.geometry('800x400')
        # apply custom layout
        View.Layout(self)
        # init theme
        self.theme: object = View.Theme(self)
        self.theme.apply('System')

        # init wmi platform
        self.provider = Provider()

        # init gui
        self.__init_gui()

        self.mainloop()

    def __init_gui(self: object) -> object:
        self.navigation: NavigationView = NavigationView(self, theme=self.theme)
        self.navigation.pack(anchor='c', fill='both', expand=True)
        # nav items
        self.navigation.add_item(Settings.NavItem(), props={'theme': self.theme})
        self.navigation.add_item(Processor.NavItem(), props={'hardware': self.provider})
        self.navigation.add_item(VideoCard.NavItem(), props={'hardware': self.provider})
        self.navigation.add_item(Memory.NavItem(), props={'hardware': self.provider})
        self.navigation.add_item(Storeage.NavItem(), props={'hardware': self.provider})



if __name__ == '__main__':
    PySpec().mainloop()
