from tkinter import ttk, StringVar, PhotoImage
from collections import namedtuple

class NavigationView(ttk.Frame):
    def __init__(self: object, parent: object, theme) -> ttk.Frame:
        super().__init__(parent)
        # pass the parent
        self.parent = parent

        # set the theme
        self.theme = theme.get_theme()
        

        self.panels: dict = {}
        self.icon_cache: dict = {}

        # nav bar stuff
        self.vav_selection: StringVar = StringVar(value='')

        self.navbar: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        # yeah, line below is .... overturtled, but for now i will leave it here ...
        ttk.Frame(self.navbar, style='dark.TFrame').pack(side='bottom', fill='x', pady=(10, 0))
        self.navbar.pack(side='left', fill='y')

        # header
        self.header: ttk.Frame = ttk.Frame(self)
        self.header_label: ttk.Label = ttk.Label(self.header, text='', style='big.TLabel', compound='left')
        self.header_label.pack(side='left', anchor='center', padx=(10, 0))
        self.header.pack(side='top', fill='x', ipady=10)
        # SCROLLABLE CONTENT

        player_content_scroll = ttk.Scrollbar(self, orient='vertical')
        player_content_scroll.pack(side='right', fill='y')

        self.content: ttk.Frame = ttk.Frame(self)

        self.content.pack(side='left', fill='both', expand=True)
        

    def add_item(self: object, item: object, props: dict = {}) -> None:
        self.icon_cache[item.name] = PhotoImage(file=fr'Resources\\Icons\\{self.theme}\\{item.icon}')
        ttk.Radiobutton(self.navbar, image=self.icon_cache[item.name], text=item.name, compound='left', value=item.name,
                        variable=self.vav_selection, command=self.__show_panel).pack(side=item.side, fill='x', padx=10, pady=(10, 0))
        self.panels[item.name] = item.page(self.content, props=props)
        self.panels[item.name].place(x=0, y=0, relwidth=1, relheight=1)

    def __show_panel(self: object) -> None:
        selected_panel: str = self.vav_selection.get()
        self.panels[selected_panel].tkraise()
        self.header_label.configure(text=selected_panel.capitalize(), image=self.icon_cache[selected_panel])
