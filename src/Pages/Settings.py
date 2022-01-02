from tkinter import ttk
from dataclasses import dataclass


class Page(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent)
        # pass parent object
        self.parent = parent
        # page layout
        Theme(self).pack(fill='x')


@dataclass
class NavItem:
    icon: str = 'settings.png'
    name: str = 'Settings'
    page: object = Page


class Theme(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        theme_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        ttk.Label(theme_panel, text='Theme', style='TLabel', compound='left').pack(
            side='left', anchor='center', fill='y')
        ttk.Radiobutton(theme_panel, text='System', style='small.TRadiobutton', value='System', command=lambda: View.Theme(
            parent.master).apply('Dark')).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Light', style='small.TRadiobutton', value='Light', command=lambda: View.Theme(
            parent.master).apply('Light')).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Dark', style='small.TRadiobutton', value='Dark', command=lambda: View.Theme(
            parent.master).apply('Dark')).pack(side='right', anchor='center', padx=(0, 10))
        theme_panel.pack(side='top', fill='x', pady=10, padx=10)
        ttk.Label(self, text='Note: You need to restart the application to see any changes!',
                  compound='left').pack(side='top', fill='x', padx=10, pady=(0, 10))
