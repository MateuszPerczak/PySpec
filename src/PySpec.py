from logging import basicConfig, error, ERROR, getLevelName
from tkinter import Tk, Frame, Label, PhotoImage, Radiobutton, Button, StringVar, Canvas, Scrollbar
from PIL import Image, ImageTk
from tkinter import ttk
from typing import ClassVar
from wmi import WMI
from os import getcwd, path
from os.path import join, isfile
from webbrowser import open as open_browser
from converter import Convert
from ctypes import c_uint32
from json import load

class App:
    def __init__(self):
        self.init_logging()
        self.main_window: ClassVar = Tk()
        self.selected: StringVar = StringVar()
        self.main_window.withdraw()
        self.main_window.geometry(f'750x450+{int(self.main_window.winfo_x() + ((self.main_window.winfo_screenwidth() - 750) / 2))}'
                        f'+{int(self.main_window.winfo_y() +((self.main_window.winfo_screenheight() - 450) / 2))}')
        self.main_window.minsize(820, 440)
        self.main_window.iconbitmap('icons\\icon.ico')
        self.main_window.configure(background='#212121')
        self.main_theme: ClassVar = ttk.Style()
        self.main_theme.theme_use('clam')
        self.main_theme.configure('TButton', background='#212121', relief='flat', font=('corbel', 20), foreground='#fff')
        self.main_theme.map('TButton', background=[('pressed', '!disabled', '#333'), ('active', '#111')])
        self.main_theme.configure('info.TButton', background='#111', relief='flat', font=('corbel', 20), foreground='#fff')
        self.main_theme.map('info.TButton', background=[('pressed', '!disabled', '#333'), ('active', '#111')])
        self.main_theme.layout('Vertical.TScrollbar', 
             [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.main_theme.configure('Vertical.TScrollbar', gripcount=0, relief='flat', background='#212121', darkcolor='#212121'
                     , lightcolor='#212121', troughcolor='#212121', bordercolor='#212121', arrowcolor='#212121')
        self.main_theme.map('Vertical.TScrollbar', background=[('pressed', '!disabled', '#333'), ('disabled', '#212121'), ('active', '#111'), ('!active', '#111')])
        self.main_window.title('PySpec')
        self.load_images()
        self.load_info()
        self.system = System()
        # frames
        self.error_frame: ClassVar = Frame(self.main_window, background='#212121')
        self.main_frame: ClassVar = Frame(self.main_window, background='#212121')
        self.select_frame: ClassVar = Frame(self.main_frame, background='#111')
        self.content_frame: ClassVar = Frame(self.main_frame, background='#212121')
        self.scrollbar: ClassVar = ttk.Scrollbar(self.main_frame)
        self.welcome_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.cpu_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.bios_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.mlb_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.ram_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.hdd_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.gpu_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.about_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.network_frame: ClassVar = Frame(self.content_frame, background='#212121')
        # display frame on app
        self.error_frame.place(x=0 ,y=0, relwidth=1, relheight=1)
        self.main_frame.place(x=0 ,y=0, relwidth=1, relheight=1)
        self.select_frame.pack(side='top', fill='x', ipady=25)
        self.content_frame.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y', expand=False)
        self.scrollbar.state(statespec=('disabled',))
        self.welcome_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.cpu_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.bios_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.mlb_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.ram_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.hdd_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.gpu_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.about_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.network_frame.place(x=0, y=0, relwidth=1, relheight=1)
        # end
        # error_window
        self.error_label: ClassVar = Label(self.error_frame, image=self.error, text='Something went wrong', compound='top'
        , font=('corbel', 35), background='#212121', foreground='#fff', anchor='center', justify='center')
        self.error_reason: ClassVar = Label(self.error_frame, text='', font=('corbel', 20), background='#212121', foreground='#e74c3c', anchor='center', justify='center')
        self.bug_button: ClassVar = ttk.Button(self.error_frame, image=self.bug, text=' Report a bug', compound='left', takefocus=False, command=self.open_issue)
        self.error_label.place(relx=0.5, rely=0.4, anchor='center', height=250, relwidth=0.8)
        self.bug_button.place(relx=0.5, rely=0.96, anchor='s')
        self.error_reason.place(relx=0.5, rely=0.7, anchor='s')
        # welcome_frame
        self.welcome_label: ClassVar = Label(self.welcome_frame, image=self.logo, font=('corbel', 40), background='#212121', foreground='#fff', anchor='center', justify='center')
        self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')
        # end
        # about frame
        info_frame: ClassVar = Frame(self.about_frame, background='#111')
        Label(info_frame, image=self.logo_small, text=' PySpec', font=('Consolas', 20), compound='left', background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=5)
        Label(info_frame, text='Version: 1.0.0\nAuthor: Mateusz Perczak\nDate: 10-04-2020\nLicence: MIT', font=('Consolas', 12), compound='left', background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)   
        ttk.Button(info_frame, image=self.bug, takefocus=False, style='info.TButton', command=self.open_issue).place(relx=1, rely=1, width=52, height=52, anchor='se')
        ttk.Button(info_frame, image=self.git, takefocus=False, style='info.TButton', command=self.open_git).place(relx=1, rely=0, width=52, height=52, anchor='ne')
        info_frame.place(relx=0.5, y=25, relwidth=0.92, height=140, anchor='n')
        # end
        # bios_frame
        try:
            self.bios_cards: ClassVar = Frame(self.bios_frame, background='#212121')
            for data in self.system.bios:
                try:
                    self.add_bios_card(data)
                except:
                    self.add_error_card(self.bios_cards)
            self.bios_cards.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # cpu_frame
        try:
            self.cpu_canvas: ClassVar = Canvas(self.cpu_frame, borderwidth=0, highlightthickness=0, background='#212121')
            self.cpu_cards: ClassVar = Frame(self.cpu_canvas, background='#212121')
            for data in self.system.cpu:
                try:
                    self.add_cpu_card(data)
                except:
                    self.add_error_card(self.cpu_cards)
            self.cpu_cards.bind('<Configure>', lambda _: self.cpu_canvas.configure(scrollregion=self.cpu_canvas.bbox('all')))
            cpu_window: ClassVar = self.cpu_canvas.create_window((0,0),window=self.cpu_cards, anchor='nw')
            self.cpu_canvas.bind('<Configure>', lambda _: self.cpu_canvas.itemconfigure(cpu_window, width=self.cpu_canvas.winfo_width(), height=self.cpu_cards.winfo_height()))
            self.cpu_canvas.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # motherboard frame
        try:
            mlb_card: ClassVar = Frame(self.mlb_frame, background='#111')
            Label(mlb_card, image=self.mlb, text=f' {self.system.motherboard.Manufacturer}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)     
            Label(mlb_card, text=f'Model: {self.system.motherboard.Product}\nChipset: {self.system.chipset.Name}\nMemory slots: {self.system.memory.MemoryDevices}\nCpu sockets: {len(self.system.cpu)}\nSerial Number: {self.system.motherboard.SerialNumber}\nVersion: {self.system.motherboard.Version}\nStatus: {self.system.motherboard.Status}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)         
            mlb_card.place(relx=0.5, y=25, relwidth=0.92, height=195, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # ram_frame
        try:
            self.ram_canvas: ClassVar = Canvas(self.ram_frame, borderwidth=0, highlightthickness=0, background='#212121')
            self.ram_cards: ClassVar = Frame(self.ram_canvas, background='#212121')
            for data in self.system.ram:
                try:
                    self.add_ram_card(data)
                except:
                    self.add_error_card(self.ram_cards)
            self.ram_cards.bind('<Configure>', lambda _: self.ram_canvas.configure(scrollregion=self.ram_canvas.bbox('all')))
            ram_window: ClassVar = self.ram_canvas.create_window((0,0),window=self.ram_cards, anchor='nw')
            self.ram_canvas.bind('<Configure>', lambda _: self.ram_canvas.itemconfigure(ram_window, width=self.ram_canvas.winfo_width(), height=self.ram_cards.winfo_height()))
            self.ram_canvas.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # hdd_frame
        try:
            self.hdd_canvas: ClassVar = Canvas(self.hdd_frame, borderwidth=0, highlightthickness=0, background='#212121')
            self.hdd_cards: ClassVar = Frame(self.hdd_canvas, background='#212121')
            for data in self.system.disk:
                try:
                    self.add_hdd_card(data)
                except:
                    self.add_error_card(self.hdd_cards)
            self.hdd_cards.bind('<Configure>', lambda _: self.hdd_canvas.configure(scrollregion=self.hdd_canvas.bbox('all')))
            hdd_window: ClassVar = self.hdd_canvas.create_window((0,0),window=self.hdd_cards, anchor='nw')
            self.hdd_canvas.bind('<Configure>', lambda _: self.hdd_canvas.itemconfigure(hdd_window, width=self.hdd_canvas.winfo_width(), height=self.hdd_cards.winfo_height()))
            self.hdd_canvas.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # gpu_frame
        try:
            self.gpu_canvas: ClassVar  = Canvas(self.gpu_frame, borderwidth=0, highlightthickness=0, background='#212121')
            self.gpu_cards: ClassVar = Frame(self.gpu_canvas, background='#212121')
            for data in self.system.gpu:
                try:
                    self.add_gpu_card(data)
                except:
                    self.add_error_card(self.gpu_cards)
            self.gpu_cards.bind('<Configure>', lambda _: self.gpu_canvas.configure(scrollregion=self.gpu_canvas.bbox('all')))
            gpu_window: ClassVar = self.gpu_canvas.create_window((0,0),window=self.gpu_cards, anchor='nw')
            self.gpu_canvas.bind('<Configure>', lambda _: self.gpu_canvas.itemconfigure(gpu_window, width=self.gpu_canvas.winfo_width(), height=self.gpu_cards.winfo_height()))
            self.gpu_canvas.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # network_frame
        try:
            self.network_canvas: ClassVar  = Canvas(self.network_frame, borderwidth=0, highlightthickness=0, background='#212121')
            self.network_cards: ClassVar = Frame(self.network_canvas, background='#212121')
            for data in self.system.network_card:
                try:
                    self.add_network_card(data)
                except:
                    self.add_error_card(self.network_cards)
            self.network_cards.bind('<Configure>', lambda _: self.network_canvas.configure(scrollregion=self.network_canvas.bbox('all')))
            network_window: ClassVar = self.network_canvas.create_window((0,0),window=self.network_cards, anchor='nw')
            self.network_canvas.bind('<Configure>', lambda _: self.network_canvas.itemconfigure(network_window, width=self.network_canvas.winfo_width(), height=self.network_cards.winfo_height()))
            self.network_canvas.place(relx=0.5, y=25, relwidth=0.92, relheight=0.97, anchor='n')
        except Exception as err_obj:
            self.dump(err_obj)
        # end
        # select_frame
        self.cpu_button: ClassVar = Radiobutton(self.select_frame, relief='flat', image=self.cpu, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='cpu', command=self.show_card)
        self.gpu_button: ClassVar = Radiobutton(self.select_frame, image=self.gpu, relief='flat', indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='gpu', command=self.show_card)
        self.ram_button: ClassVar = Radiobutton(self.select_frame, image=self.ram, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='ram', command=self.show_card)
        self.mlb_button: ClassVar = Radiobutton(self.select_frame, image=self.mlb, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='mlb', command=self.show_card)
        self.hdd_button: ClassVar = Radiobutton(self.select_frame, image=self.hdd, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='hdd', command=self.show_card)
        self.bios_button: ClassVar = Radiobutton(self.select_frame, image=self.bios, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='bios', command=self.show_card)
        self.network_button: ClassVar = Radiobutton(self.select_frame, image=self.network, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='network', command=self.show_card)
        self.about_button: ClassVar = Radiobutton(self.select_frame, image=self.about, indicatoron=False, bd=0, background='#111'
        , selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', variable=self.selected, value='about', command=self.show_card)
        self.cpu_button.place(x=0, y=0, width=52, relheight=1)
        self.gpu_button.place(x=52, y=0, width=52, relheight=1)
        self.ram_button.place(x=104, y=0, width=52, relheight=1)
        self.mlb_button.place(x=156, y=0, width=52, relheight=1)
        self.hdd_button.place(x=208, y=0, width=52, relheight=1)
        self.bios_button.place(x=260, y=0, width=52, relheight=1)
        self.network_button.place(x=312, y=0, width=52, relheight=1)
        self.about_button.place(relx=1, rely=1, width=52, relheight=1, anchor='se')
        # end
        self.welcome_frame.tkraise()
        self.main_window.deiconify()
        self.main_window.bind('<MouseWheel>', self.on_mouse)
        self.main_window.mainloop()
    
    def on_mouse(self, event):
        SELECTED: str = self.selected.get()
        if SELECTED == 'cpu':
            self.cpu_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif SELECTED == 'ram':
            self.ram_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif SELECTED == 'hdd':
            self.hdd_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif SELECTED == 'gpu':
            self.gpu_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif SELECTED == 'network':
            self.network_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def load_images(self) -> None:
        try:
            self.error: ClassVar = ImageTk.PhotoImage(Image.open('icons\\error.png').resize((85, 85)))
            self.cpu: ClassVar = ImageTk.PhotoImage(Image.open('icons\\cpu.png').resize((35, 35)))
            self.gpu: ClassVar = ImageTk.PhotoImage(Image.open('icons\\gpu.png').resize((35, 35)))
            self.ram: ClassVar = ImageTk.PhotoImage(Image.open('icons\\ram.png').resize((35, 35)))
            self.mlb: ClassVar = ImageTk.PhotoImage(Image.open('icons\\mlb.png').resize((35, 35)))
            self.hdd: ClassVar = ImageTk.PhotoImage(Image.open('icons\\hdd.png').resize((35, 35)))
            self.logo: ClassVar = ImageTk.PhotoImage(Image.open('icons\\logo.png').resize((85, 85)))
            self.bios: ClassVar = ImageTk.PhotoImage(Image.open('icons\\bios.png').resize((35, 35)))
            self.bug: ClassVar = ImageTk.PhotoImage(Image.open('icons\\bug.png').resize((35, 35)))
            self.git: ClassVar = ImageTk.PhotoImage(Image.open('icons\\git.png').resize((35, 35)))
            self.about: ClassVar = ImageTk.PhotoImage(Image.open('icons\\about.png').resize((35, 35)))
            self.network: ClassVar = ImageTk.PhotoImage(Image.open('icons\\network.png').resize((35, 35)))
            self.logo_small: ClassVar = ImageTk.PhotoImage(Image.open('icons\\logo_small.png').resize((35, 35)))
        except Exception as err_obj:
            self.dump(err_obj)
    
    def dump(self, err_obj) -> None:
        self.error_reason.configure(text=f'Error: {getLevelName(err_obj)}')
        error(err_obj, exc_info=True)
        self.error_frame.tkraise()
    
    def init_logging(self) -> None:
        with open('errors.log','w') as file:
            file.write('')
        basicConfig(filename='errors.log', level=ERROR)

    def open_issue(self) -> None:
        open_browser('https://github.com/losek1/PySpec/issues', new=0, autoraise=True)
    
    def open_git(self) -> None:
        open_browser('https://github.com/losek1/PySpec', new=0, autoraise=True)
    
    def show_card(self) -> None:
        SELECTED: str = self.selected.get()
        if SELECTED == 'cpu':
            self.cpu_frame.lift()
            self.cpu_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.cpu_canvas.yview)
        elif SELECTED == 'mlb':
            self.mlb_frame.lift()
            self.scrollbar.state(statespec=('disabled',))
        elif SELECTED == 'bios':
            self.bios_frame.lift()
            self.scrollbar.state(statespec=('disabled',))
        elif SELECTED == 'ram':
            self.ram_frame.lift()
            self.ram_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.ram_canvas.yview)
        elif SELECTED == 'hdd':
            self.hdd_frame.lift()
            self.hdd_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.hdd_canvas.yview)
        elif SELECTED == 'gpu':
            self.gpu_frame.lift()
            self.gpu_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.gpu_canvas.yview)
        elif SELECTED == 'about':
            self.about_frame.lift()
            self.scrollbar.state(statespec=('disabled',))
        elif SELECTED == 'network':
            self.network_frame.lift()
            self.network_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.network_canvas.yview)
        else:
            self.error_frame.lift()
    
    def load_info(self):
        try:
            if path.isfile('slots.json'):
                with open('slots.json', 'r') as file:
                    self.slots: dict = load(file)
        except Exception as err_obj:
            self.dump(err_obj)

    def add_bios_card(self, data) -> None:
        if data.PrimaryBIOS:
            bios_type = 'Primary BIOS'
        else:
            bios_type = 'Secondary BIOS'
        bios_card: ClassVar = Frame(self.bios_cards, background='#111')
        Label(bios_card, image=self.bios, text=f' {bios_type}', font=('Consolas', 20), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
        Label(bios_card, text=f'Brand: {data.Manufacturer}\nVersion: {data.BIOSVersion[1]}\nDate: {data.ReleaseDate[4:6]}-{data.ReleaseDate[6:8]}-{data.ReleaseDate[0:4]}\nStatus: {data.Status}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)
        bios_card.pack(side='top', fill='x', ipady=70, pady=(0, 25))
    
    def add_cpu_card(self, data) -> None:
        cpu_card: ClassVar = Frame(self.cpu_cards, background='#111')
        Label(cpu_card, image=self.cpu, text=f' {data.Name}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
        Label(cpu_card, text=f'{data.Description}\nArchitecture: {data.DataWidth} Bit\nCores: {data.NumberOfCores}\nThreads: {data.ThreadCount}\nClock Speed: {data.CurrentClockSpeed} Mhz\nMax Clock Speed: {data.MaxClockSpeed} Mhz\nL2 Cache Size: {Convert.KilobytesToMegabytes(data.L2CacheSize)}\nL3 Cache Size: {Convert.KilobytesToMegabytes(data.L3CacheSize)}\nStatus: {data.Status}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)
        cpu_card.pack(side='top', fill='x', ipady=115, pady=(0, 25))
    
    def add_ram_card(self, data) -> None:
        ram_card: ClassVar = Frame(self.ram_cards, background='#111')
        Label(ram_card, image=self.ram, text=f' {data.Manufacturer} {data.PartNumber.rstrip()}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
        Label(ram_card, text=f'Capacity: {Convert.BytesToGigabytes(int(data.Capacity))}\nPart Number: {data.SerialNumber}\nSpeed: {data.Speed} Mhz\nVoltage: {data.ConfiguredVoltage/ 1000} V\nSlot: {data.DeviceLocator}\nForm Factor: {self.slots[str(data.FormFactor)]}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)
        ram_card.pack(side='top', fill='x', ipady=85, pady=(0, 25))
    
    def add_hdd_card(self, data) -> None:
        if data.Size:
            hdd_card: ClassVar = Frame(self.hdd_cards, background='#111')
            Label(hdd_card, image=self.hdd, text=f' {data.Caption}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
            Label(hdd_card, text=f'Capacity: {Convert.BytesToGigabytes(int(data.Size))}\nType: {data.MediaType}\nSerial Number: {data.SerialNumber.strip()}\nFirmware Version: {data.FirmwareRevision.strip()}\nStatus: {data.Status}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)
            hdd_card.pack(side='top', fill='x', ipady=80, pady=(0, 25))
    
    def add_gpu_card(self, data):
        gpu_card: ClassVar = Frame(self.gpu_cards, background='#111')
        Label(gpu_card, image=self.gpu, text=f' {data.Name}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
        Label(gpu_card, text=f'Memory Size: {Convert.BytesToGigabytes(c_uint32(data.AdapterRAM).value)}\nDriver Date: {data.DriverDate[6:8]}-{data.DriverDate[4:6]}-{data.DriverDate[0:4]}\nDriver Version: {data.DriverVersion}\nResolution: {data.CurrentHorizontalResolution}X{data.CurrentVerticalResolution}\nMax Refresh Rate: {data.MaxRefreshRate} Hz\nRefresh Rate: {data.CurrentRefreshRate} Hz\nStatus: {data.Status}', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)    
        gpu_card.pack(side='top', fill='x', ipady=95, pady=(0, 25))

    def add_network_card(self, data):
        network_card: ClassVar = Frame(self.network_cards, background='#111')
        Label(network_card, image=self.network, text=f' {data.Name}', font=('Consolas', 16), compound='left', background='#111', foreground='#fff', anchor='center', justify='center').place(x=5, y=5)
        Label(network_card, text=f'Manufacturer: {data.Manufacturer}\nAdapter Type: {data.AdapterType}\nMAC Address: {data.MACAddress}\nSpeed: {int(data.Speed) / 1000000} Mbps', font=('Consolas', 12), background='#111', foreground='#fff', anchor='w', justify='left').place(x=5, y=50)    
        network_card.pack(side='top', fill='x', ipady=70, pady=(0, 25))

    def add_error_card(self, frame):
        error_card: ClassVar = Frame(frame, background='#111')
        Label(error_card, image=self.error, text='Error: Unable to detect device', font=('Consolas', 16), compound='top', background='#111', foreground='#e74c3c', anchor='center', justify='center').place(relx=0.5, rely=0.5, anchor='center')
        error_card.pack(side='top', fill='x', ipady=70, pady=(0, 25))

class System:
    def __init__(self):
        COMPUTER: ClassVar = WMI()
        self.network_card = []
        for network_card in COMPUTER.Win32_NetworkAdapter(NetConnectionID='ethernet'):
            self.network_card.append(network_card)
        devices: list = []
        self.cpu: list = []
        for cpu in COMPUTER.Win32_Processor():
            self.cpu.append(cpu)
        if self.cpu[0].Manufacturer == 'GenuineIntel':
            devices = COMPUTER.win32_pnpentity(Manufacturer='INTEL', PNPClass='System')
            for device in devices:
                if 'Chipset' in device.Name.split():
                    self.chipset: ClassVar = device
        else:
            self.device = COMPUTER.win32_pnpentity(Manufacturer='AMD')
            for device in devices:
                if 'Chipset' in device.Name.split():
                    self.chipset: ClassVar = device
        self.motherboard: ClassVar = COMPUTER.Win32_BaseBoard()[0]
        self.memory: ClassVar = COMPUTER.Win32_PhysicalMemoryArray()[0]
        self.bios: list = []
        for bios in COMPUTER.Win32_BIOS():
            self.bios.append(bios)
        self.gpu: list = []
        for gpu in COMPUTER.Win32_VideoController():
            self.gpu.append(gpu)
        self.disk: list = []
        for drive in COMPUTER.Win32_DiskDrive():
            self.disk.append(drive)
        self.ram: list = []
        for memory in COMPUTER.Win32_PhysicalMemory():
            self.ram.append(memory)


if __name__ == '__main__':
    App()