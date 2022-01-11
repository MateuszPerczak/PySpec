from tkinter import ttk
from dataclasses import dataclass
from Components.Converter import BytesToGigabytes, MillivoltsToVolts
from Components.ErrorHandler import ErrMsg

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout
        for memory in props['hardware'].get_rams():
            try:
                MemoryCard(self, memory).pack(fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))

class MemoryCard(ttk.Frame):
    def __init__(self: object, parent: object, memory: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=f'{memory["manufacturer"]} {memory["part_number"]}').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Capacity: {BytesToGigabytes(memory["capacity"])}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Speed: {memory["speed"]} MHz', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Voltage: {MillivoltsToVolts(memory["voltage"])}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Type: {memory["type"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Slot: {memory["slot"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Serial No.: {memory["serial"]}', style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))

@dataclass
class NavItem:
    icon: str = 'memory.png'
    name: str = 'Memory'
    page: object = Page
    side: str = 'top'