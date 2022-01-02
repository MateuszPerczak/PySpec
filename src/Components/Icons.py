from tkinter import PhotoImage


def Brush(theme: str) -> PhotoImage:
    return PhotoImage(file=fr'Resources\\Icons\\{theme}\\brush.png')
