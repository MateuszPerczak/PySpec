from tkinter import ttk, StringVar, PhotoImage, Canvas, Event
from collections import namedtuple

class NavigationView(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent)
        # pass the parent
        self.parent = parent

        # set the theme
        self.theme: object = theme
        
        # navigatoin variables
        self.radiobuttons: dict = {}
        self.panels: dict = {}
        self.icon_cache: dict = {}

        # acceleration
        self.acceleration: float = 1.0

        # nav bar stuff
        self.vav_selection: StringVar = StringVar(value='')

        self.navbar: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        # yeah, line below is .... overturtled, but for now i will leave it here ...
        ttk.Frame(self.navbar, style='dark.TFrame').pack(side='bottom', fill='x', pady=(10, 0))
        self.navbar.pack(side='left', fill='y')

        # scrollbar
        scrollbar: ttk.Scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # header
        self.header: ttk.Frame = ttk.Frame(self)
        self.header_label: ttk.Label = ttk.Label(self.header, text='', style='big.TLabel', compound='left')
        self.header_label.pack(side='left', anchor='center', padx=(10, 0))
        self.header.pack(side='top', fill='x', ipady=10)
        # scrollable frame

        self.canvas: Canvas = Canvas(self, bg=self.master['background'], bd=0, highlightthickness=0, yscrollcommand=scrollbar.set, takefocus=False)
        # link scrollbar to canvas
        scrollbar.configure(command=self.canvas.yview)
        
        # create content frame
        self.content: ttk.Frame = ttk.Frame(self.canvas)

        self.content.bind('<Expose>', lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # create window insode a canvas
        self.content_window = self.canvas.create_window((0, 0), window=self.content, anchor='nw')

        self.canvas.bind('<Expose>', lambda _: self.canvas.itemconfigure(self.content_window, width=self.canvas.winfo_width(), height=0))

        # pack everything
        self.canvas.pack(side='left', fill='both', expand=True)

        # bind mouse scroll to move canvas
        self.master.bind('<MouseWheel>', self.__on_wheel)

        # bind theme change
        theme.bind(self.__on_theme_changed)
        

    def add_item(self: object, item: object, props: dict = {}) -> None:
        # load both icons
        self.icon_cache[item.name] = {
            'Dark': PhotoImage(file=fr'Resources\\Icons\\Dark\\{item.icon}'),
            'Light': PhotoImage(file=fr'Resources\\Icons\\Light\\{item.icon}')
        }
        # create radiobutton
        self.radiobuttons[item.name] = ttk.Radiobutton(self.navbar, image=self.icon_cache[item.name][self.theme.get_theme()], text=item.name, compound='left', value=item.name, variable=self.vav_selection, command=self.__show_panel)
        self.radiobuttons[item.name].pack(side=item.side, fill='x', padx=10, pady=(10, 0))
        # store page in dict
        self.panels[item.name] = item.page(self.content, props=props)

    def __show_panel(self: object) -> None:
        selected_panel: str = self.vav_selection.get()
        for panel in self.panels:
            if panel != selected_panel:
                self.panels[panel].pack_forget()
        self.panels[selected_panel].pack(side='top', fill='both', expand=True)
        self.header_label.configure(text=selected_panel.capitalize(), image=self.icon_cache[selected_panel][self.theme.get_theme()])
        # move content to top
        self.canvas.yview_moveto(0)

    def __on_wheel(self: object, event: Event) -> None:
        self.canvas.yview_scroll(int(-self.acceleration*(event.delta/120)), 'units')

    
    def __on_theme_changed(self: object, theme: str) -> None:
        # chanhe canvas colors
        self.canvas['bg'] = self.theme.get_colors(theme)[1]
        # change radiobuttons icons
        for button in self.radiobuttons:
            self.radiobuttons[button].configure(image=self.icon_cache[button][theme])
        # update header
        selected_panel: str = self.vav_selection.get()
        self.header_label.configure(text=selected_panel.capitalize(), image=self.icon_cache[selected_panel][self.theme.get_theme()])

