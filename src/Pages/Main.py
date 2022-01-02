from tkinter import ttk


class Page(ttk.Frame):
    def __init__(self: object, parent: object) -> ttk.Frame:
        super().__init__(parent)
        # page layout
        ttk.Label(self, text='Welocme to PySpec!', style='center.TLabel').pack(
            anchor='c', expand=True, fill='both')
