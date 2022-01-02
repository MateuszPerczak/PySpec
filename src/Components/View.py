from tkinter import PhotoImage, Tk, ttk


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
        self.colors: dict = {'Dark': ['#000', '#111', '#222', '#ecf0f1'], 'Light': [
            '#fff', '#ecf0f1', '#ecf0f1', '#000']}

    def apply(self: object, theme: str) -> None:
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
        # rqadio button
        self.parent.layout.configure('TRadiobutton', background=self.colors[theme][0], relief='flat', font=(
            'catamaran 13 bold'), foreground=self.colors[theme][3], anchor='w', padding=5, width=12)
        self.parent.layout.map('TRadiobutton', background=[('pressed', '!disabled', self.colors[theme][1]), (
            'active', self.colors[theme][1]), ('selected', self.colors[theme][1])])


class Icons:
    def __init__(self: object, parent: Tk) -> object:
        # pass parent object
        self.parent = parent