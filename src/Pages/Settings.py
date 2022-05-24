from tkinter import ttk, StringVar, PhotoImage, DoubleVar, Event
from dataclasses import dataclass


class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        # pass parent object
        self.parent = parent
        # page layout
        Acceleration(self, props).pack(fill='x', padx=10, pady=(0, 10))
        Theme(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))
        About(self, props['theme']).pack(fill='x', padx=10, pady=(0, 10))


@dataclass
class NavItem:
    icon: str = 'settings.png'
    name: str = 'Settings'
    page: object = Page
    side: str = 'bottom'


class Theme(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable
        self.theme: StringVar = StringVar(value=theme.get_internal_theme())

        self.icon_cache = {
            'info': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\info.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\info.png')

            },
            'brush': {
                'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\brush.png'),
                'Light': PhotoImage(file=r'Resources\\Icons\\Light\\brush.png')
            },
        }

        theme_panel: ttk.Frame = ttk.Frame(self, style='dark.TFrame')
        self.header: ttk.Label = ttk.Label(theme_panel, image=self.icon_cache['brush'][theme.get_theme(
        )], text='Theme', style='TLabel', compound='left')
        self.header.pack(side='left', anchor='center', fill='y')
        ttk.Radiobutton(theme_panel, text='System', style='small.TRadiobutton', value='System', command=lambda: theme.apply(
            'Dark'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Light', style='small.TRadiobutton', value='Light', command=lambda: theme.apply(
            'Light'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        ttk.Radiobutton(theme_panel, text='Dark', style='small.TRadiobutton', value='Dark', command=lambda: theme.apply(
            'Dark'), variable=self.theme).pack(side='right', anchor='center', padx=(0, 10))
        theme_panel.pack(side='top', fill='x', pady=10, padx=10)
        self.info: ttk.Label = ttk.Label(self, image=self.icon_cache['info'][theme.get_theme()], text='Note: You need to restart the application to see any changes!',
                                         compound='left')
        self.info.pack(side='top', fill='x', padx=10, pady=(0, 10))

        # bind theme change
        theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: object) -> None:
        self.info.configure(image=self.icon_cache['info'][theme])
        self.header.configure(image=self.icon_cache['brush'][theme])


class Acceleration(ttk.Frame):
    def __init__(self: object, parent: object, props: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable
        self.acceleration: DoubleVar = DoubleVar(value=1.0)
        self.navigation = props['navigation']
        self.theme = props['theme']
        self.icon_cache = {
            'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\scroll.png'),
            'Light': PhotoImage(file=r'Resources\\Icons\\Light\\scroll.png')
        }

        self.header: ttk.Label = ttk.Label(self, image=self.icon_cache[self.theme.get_theme(
        )], text='Wheel acceleration', compound='left')
        self.header.pack(side='left', anchor='c', fill='y', pady=10, padx=10)
        ttk.Label(self, text='Fast').pack(side='right',
                                          anchor='c', fill='y', pady=10, padx=10)
        ttk.Scale(self, variable=self.acceleration, from_=1, to=8, command=self.__on_acceleration).pack(
            side='right', anchor='c', fill='x', ipadx=20)
        ttk.Label(self, text='Slow').pack(side='right',
                                          anchor='c', fill='y', pady=10, padx=10)
        # bind theme change
        self.theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: str) -> None:
        self.header.configure(image=self.icon_cache[theme])

    def __on_acceleration(self: object, event: Event) -> None:
        self.navigation.acceleration = self.acceleration.get()


class About(ttk.Frame):
    def __init__(self: object, parent: object, theme: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        # local variable

        self.icon_cache = {
            'Dark': PhotoImage(file=r'Resources\\Icons\\Dark\\info.png'),
            'Light': PhotoImage(file=r'Resources\\Icons\\Light\\info.png')
        }

        self.header: ttk.Label = ttk.Label(self, image=self.icon_cache[theme.get_theme(
        )], text='About PySpec', style='TLabel', compound='left')
        self.header.pack(side='top', fill='x', padx=10, pady=10)
        ttk.Label(self, text='Version: 1.0.0 Build: 120122',
                  style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Author: Mateusz Perczak',
                  style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text='Icons: Icons8', style='small.TLabel').pack(
            side='top', fill='x', padx=10, pady=(0, 10))
        # bind theme change
        theme.bind(self.__on_theme_changed)

    def __on_theme_changed(self: object, theme: str) -> None:
        self.header.configure(image=self.icon_cache[theme])
