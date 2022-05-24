from tkinter import Tk
from Pages import Settings, Processor, Memory, Storage, VideoCard, Motherboard, Network
from Components import View
from Components.NavigationView import NavigationView
from Components.Inithandler import InitPage
from Components.SysInfo import Provider
# from Components.Debugger import Debugger


class PySpec(Tk):
    def __init__(self: object) -> object:
        super().__init__()
        self.title('PySpec')
        self.geometry('900x500')
        self.minsize(800, 400)
        self.iconbitmap(r'Resources\\Icons\\Static\\icon.ico')
        # apply custom layout
        View.Layout(self)
        # init theme
        self.theme: object = View.Theme(self)
        self.theme.apply('System')

        self.init_page: InitPage = InitPage(self)
        self.init_page.pack(fill='both', expand=True)

        self.after(100, self.__init)
        self.mainloop()

    def __init(self: object) -> object:
        # init wmi platform
        self.provider = Provider()
        # unload loading page
        self.init_page.pack_forget()
        del self.init_page
        # init gui
        self.__init_gui()

    def __init_gui(self: object) -> object:
        self.navigation: NavigationView = NavigationView(
            self, theme=self.theme)
        self.navigation.pack(anchor='c', fill='both', expand=True)
        # nav items
        self.navigation.add_item(Settings.NavItem(), props={
                                 'theme': self.theme, 'navigation': self.navigation})
        self.navigation.add_item(Processor.NavItem(), props={
                                 'hardware': self.provider})
        self.navigation.add_item(VideoCard.NavItem(), props={
                                 'hardware': self.provider})
        self.navigation.add_item(Memory.NavItem(), props={
                                 'hardware': self.provider})
        self.navigation.add_item(Motherboard.NavItem(), props={
                                 'hardware': self.provider})
        self.navigation.add_item(Storage.NavItem(), props={
                                 'hardware': self.provider})
        self.navigation.add_item(Network.NavItem(), props={
                                 'hardware': self.provider})
        # select forst page
        self.navigation.select('Processor')


if __name__ == '__main__':
    PySpec().mainloop()
