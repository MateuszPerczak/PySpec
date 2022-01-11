from tkinter import Tk, ttk
from typing import Callable
from Components.SystemTheme import get_theme

class Layout:
    def __init__(self: object, parent: Tk) -> object:
        # pass parent object
        self.parent = parent

        # init theme object
        self.parent.layout = ttk.Style()
        # set theme to clam
        self.parent.layout.theme_use('clam')
        # button
        self.parent.layout.layout('TButton', [('Button.padding', {
                                  'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})])
        # radiobutton
        self.parent.layout.layout('TRadiobutton', [('Radiobutton.padding', {
                                  'sticky': 'nswe', 'children': [('Radiobutton.label', {'sticky': 'nswe'})]})])
        # scrollbar
        self.parent.layout.layout('Vertical.TScrollbar', [('Vertical.Scrollbar.trough', {'children': [
                                  ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        # entry
        self.parent.layout.layout('TEntry', [('Entry.padding', {
                                  'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})])


class Theme:
    def __init__(self: object, parent: Tk) -> None:
        # pass parent object
        self.parent = parent
        self.colors: dict = {'Dark': ['#111', '#212121', '#333', '#fff'], 'Light': [
            '#fff', '#ecf0f1', '#ecf0f1', '#000']}
        # get system theme
        self.system_theme: str = get_theme()
        self.colors['System'] = self.colors[self.system_theme]
        # set default applied theme
        self.applied_theme: str = 'Light'
        # methode list
        self.__binded_methods: list = []


    def apply(self: object, theme: str) -> None:
        self.applied_theme = theme
        # pass parent object
        self.parent.configure(background=self.colors[theme][1])
        # frames
        self.parent.layout.configure(
            'TFrame', background=self.colors[theme][1])
        self.parent.layout.configure(
            'dark.TFrame', background=self.colors[theme][0])
        # label
        self.parent.layout.configure('TLabel', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 12 bold'), foreground=self.colors[theme][3])
        self.parent.layout.configure('center.TLabel', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 12 bold'), foreground=self.colors[theme][3], anchor='c')
        self.parent.layout.configure(
            'big.TLabel', background=self.colors[theme][1], font=('catamaran 16 bold'))
        self.parent.layout.configure(
            'small.TLabel', background=self.colors[theme][0], font=('catamaran 10 bold'))
        # rqadio button
        self.parent.layout.configure('TRadiobutton', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 13 bold'), foreground=self.colors[theme][3], anchor='w', padding=5, width=12)
        self.parent.layout.map('TRadiobutton', background=[('pressed', '!disabled', self.colors[theme][1]), (
            'active', self.colors[theme][1]), ('selected', self.colors[theme][1])])
        self.parent.layout.configure('small.TRadiobutton',
                              anchor='center', padding=5, width=8)
        # scrollbar
        self.parent.layout.configure('Vertical.TScrollbar', gripcount=0, relief='flat', background=self.colors[theme][1], darkcolor=self.colors[theme][1], lightcolor=self.colors[theme][1], troughcolor=self.colors[theme][1], bordercolor=self.colors[theme][1])
        self.parent.layout.map('Vertical.TScrollbar', background=[('pressed', '!disabled', self.colors[theme][0]), (
            'disabled', self.colors[theme][1]), ('active', self.colors[theme][0]), ('!active', self.colors[theme][0])])

        # scale
        self.parent.layout.configure('Horizontal.TScale', troughcolor=self.colors[theme][0], background=self.colors[theme][1], relief='flat', gripcount=0, darkcolor=self.colors[theme][0], lightcolor=self.colors[theme][0], bordercolor=self.colors[theme][0])
        self.parent.layout.map('Horizontal.TScale', background=[('pressed', '!disabled', self.colors[theme][2]), ('active', self.colors[theme][2])])
        # raise event
        self.theme_changed(theme)


    def get_theme(self: object) -> str:
        if self.applied_theme == 'System':
            return self.system_theme
        return self.applied_theme

    def get_internal_theme(self: object) -> str:
        return self.applied_theme

    def theme_changed(self: object, theme: str) -> None:
        for methode in self.__binded_methods:
            methode(theme)

    def bind(self: object, methode: Callable) -> None:
        self.__binded_methods.append(methode)

    def get_colors(self: object, theme: str) -> list:
        return self.colors[theme]