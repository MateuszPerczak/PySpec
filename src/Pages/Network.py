from tkinter import ttk
from dataclasses import dataclass
from Components.ErrorHandler import ErrMsg
from Components.Converter import KilobytesToMegabytes

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        for network_adapter in props['hardware'].get_network_adapters():
            try:
                NetworkCard(self, network_adapter).pack(
                    fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))

class NetworkCard(ttk.Frame):
    def __init__(self: object, parent: object, adapter: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=adapter["name"]).pack(
            side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Manufacturer: {adapter["manufacturer"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Type: {adapter["type"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Mac address: {adapter["mac_address"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10, pady=(0, 10))

@dataclass
class NavItem:
    icon: str = 'network.png'
    name: str = 'Network'
    page: object = Page
    side: str = 'top'
