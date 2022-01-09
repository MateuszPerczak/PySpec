from tkinter import ttk
from dataclasses import dataclass


class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout





@dataclass
class NavItem:
    icon: str = 'gpu.png'
    name: str = 'Video Card'
    page: object = Page
    side: str = 'top'

# get_gpus