from tkinter import ttk
from dataclasses import dataclass
from Components.Converter import KilobytesToGigabytes
from Components.ErrorHandler import ErrMsg

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout
        # get mlb info
        try:
            MotherBoard(self, props['hardware'].get_motherboard()).pack(fill='x', padx=10, pady=(0, 10))
        except Exception as err_obj:
            ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))
        # get bios info
        for bios in props['hardware'].get_bios():
            try:
                BiosCard(self, bios).pack(fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))

class MotherBoard(ttk.Frame):
    def __init__(self: object, parent: object, motherboard: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=f'{motherboard["manufacturer"]} {motherboard["product"]}').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Chipset: {motherboard["chipset"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Memory slots: {motherboard["memory_slots"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Memory max capacity: {KilobytesToGigabytes(motherboard["max_capacity"])}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Serial No.: {motherboard["part_number"]}', style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))

class BiosCard(ttk.Frame):
    def __init__(self: object, parent: object, bios: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text='Bios').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Manufacturer: {bios["manufacturer"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Version: {bios["version"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Release date: {bios["release"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Primary: {bios["primary"]}', style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))

@dataclass
class NavItem:
    icon: str = 'motherboard.png'
    name: str = 'Motherboard'
    page: object = Page
    side: str = 'top'