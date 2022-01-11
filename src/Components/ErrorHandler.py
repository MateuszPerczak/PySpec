from tkinter import ttk
from traceback import format_exc

class ErrMsg(ttk.Frame):
    def __init__(self: object, parent: object, err_obj: object) -> ttk.Frame:
        super().__init__(parent, style='dark.TFrame')
        ttk.Label(self, text='Error').pack(side='top', fill='x', padx=10, pady=(10, 0))
        ttk.Label(self, text='Something went wrong', style='small.TLabel').pack(side='top', fill='x', padx=10)
        ttk.Label(self, text=format_exc().split("\n")[-2], style='small.TLabel').pack(side='top', fill='x', padx=10, pady=(0, 10))
        