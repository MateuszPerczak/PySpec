from tkinter import ttk
from dataclasses import dataclass
from Components.Converter import MegabytesToGigabytes
from Components.ErrorHandler import ErrMsg

class Page(ttk.Frame):
    def __init__(self: object, parent: object, props: dict = {}) -> ttk.Frame:
        super().__init__(parent)
        # page layout
        for video_card in props['hardware'].get_gpus():
            try:
                VideoCard(self, video_card).pack(fill='x', padx=10, pady=(0, 10))
            except Exception as err_obj:
                ErrMsg(self, err_obj).pack(fill='x', padx=10, pady=(0, 10))

class VideoCard(ttk.Frame):
    def __init__(self: object, parent: object, video_card: dict) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text=f'{video_card["name"]}').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text=f'Vram: {MegabytesToGigabytes(video_card["total_memory"])}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Temperature: {video_card["temp"]} °C', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Resolution: {video_card["resolution"][0]}x{video_card["resolution"][1]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Driver version: {video_card["driver_version"]}', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=f'Current refresh: {video_card["refresh_rate"]} Hz', style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))

@dataclass
class NavItem:
    icon: str = 'gpu.png'
    name: str = 'Video Card'
    page: object = Page
    side: str = 'top'