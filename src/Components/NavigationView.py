from tkinter import ttk, StringVar


class NavigationView(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent)
        # pass the parent
        self.parent = parent

        self.panels: dict = {}

        # nav bar stuff
        self.vav_selection: StringVar = StringVar(value='')

        self.navbar: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        self.navbar.pack(side='left', fill='y')

        self.content: ttk.Frame = ttk.Frame(self)

        self.content.pack(side='left', fill='both', expand=True)

    def add_item(self: object, item: object) -> None:
        ttk.Radiobutton(self.navbar, text=item.name, compound='left', value=item.name,
                        variable=self.vav_selection, command=self.__show_panel).pack(side='top', fill='x', padx=10, pady=(10, 0))
        self.panels[item.name] = item.page(self.content)
        self.panels[item.name].place(x=0, y=0, relwidth=1, relheight=1)

    def __show_panel(self: object) -> None:
        self.panels[self.vav_selection.get()].tkraise()
