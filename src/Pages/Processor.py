from tkinter import ttk
from dataclasses import dataclass
from Components.Converter import MHzToGHz, KilobytesToMegabytes
from Components.ErrorHandler import ErrMsg


class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict) -> ttk.Frame:
        super().__init__(parent)
        for processor in props['hardware'].get_cpus():
            try:
                ProcessorCard(self, processor).pack(
                    fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))


class ProcessorCard(ttk.Frame):
    def __init__(self: object, parent: object, processor: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=processor["name"]).pack(
            side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=processor["description"], style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Manufacturer: {processor["manufacturer"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Family: {processor["family"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Clock speed: {MHzToGHz(processor["clock_speed"])}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Architecture: {processor["architecture"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Cores: {processor["cores"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Threads: {processor["threads"]}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'L2 Cache: {KilobytesToMegabytes(processor["cache_l2"])}', style='small.TLabel').pack(
            side='top', fill='x', padx=10)
        ttk.Label(self, text=f'L3 Cache: {KilobytesToMegabytes(processor["cache_l3"])}', style='small.TLabel').pack(
            side='top', fill='x', padx=10, pady=(0, 10))


@dataclass
class NavItem:
    icon: str = 'processor.png'
    name: str = 'Processor'
    page: object = Page
    side: str = 'top'
