from tkinter import ttk
from dataclasses import dataclass

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout


@dataclass
class NavItem:
    icon: str = 'disk.png'
    name: str = 'Storeage'
    page: object = Page
    side: str = 'top'