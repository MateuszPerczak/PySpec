from tkinter import ttk
from dataclasses import dataclass
from Components.ErrorHandler import ErrMsg
from Components.Converter import BytesToGigabytes

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout
        for drive in props['hardware'].get_storage():
            try:
                DriveCard(self, drive).pack(fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))

class DriveCard(ttk.Frame):
    def __init__(self: object, parent: object, drive: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=f'{drive["model"]}').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Size: {BytesToGigabytes(drive["size"])}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Firmware: {drive["firmware"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Serial No.: {drive["serial"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Capabilities: {drive["supports"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Id: {drive["id"]}', style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))

@dataclass
class NavItem:
    icon: str = 'disk.png'
    name: str = 'Storeage'
    page: object = Page
    side: str = 'top'