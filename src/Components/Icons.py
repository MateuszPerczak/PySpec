from tkinter import PhotoImage


def Brush(theme: str) -> PhotoImage:
    return PhotoImage(file=fr'Resources\\Icons\\{theme}\\brush.png')


def Settings(theme: str) -> PhotoImage:
    return PhotoImage(file=fr'Resources\\Icons\\{theme}\\settings.png')
