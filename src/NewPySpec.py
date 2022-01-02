from tkinter import Tk
from Pages import Settings, Main
from Components import View
from Components.NavigationView import NavigationView


class PySpec(Tk):
    def __init__(self: object) -> object:
        super().__init__()
        self.title('PySpec')
        self.geometry('800x400')
        View.Layout(self)
        View.Theme(self).apply('Dark')

        self.navigation: NavigationView = NavigationView(self)
        self.navigation.pack(anchor='c', fill='both', expand=True)

        self.navigation.add_item(Settings.NavItem())

        self.mainloop()


if __name__ == '__main__':
    PySpec().mainloop()
