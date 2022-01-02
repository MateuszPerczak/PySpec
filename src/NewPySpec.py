from tkinter import Tk
from Pages import Settings
from Components import View


class PySpec(Tk):
    def __init__(self: object) -> object:
        super().__init__()
        self.title('PySpec')
        self.geometry('800x400')
        View.Layout(self)
        View.Theme(self).apply('Dark')

        self.settings = Settings.Page(self)
        self.settings.pack(fill='both', expand=True)

        self.mainloop()


if __name__ == '__main__':
    PySpec().mainloop()
