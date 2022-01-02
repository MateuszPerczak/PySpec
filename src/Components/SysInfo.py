try:
    from wmi import WMI
    from GPUtil import getGPUs
    from json import load, dump
    from os.path import isfile
except ImportError as err_obj:
    exit(err_obj)


class Provider:
    def __init__(self: object) -> None:
        # prepare data
        # wmi is kinda slow
        self.wmi_object: WMI = WMI()
        # for disk in self.wmi_object.Win32_DiskDrive():
        #     print(disk)
        self.gpu_list: list = getGPUs()
        # load data
        self.load_data()

    def load_data(self: object) -> None:
        # load cpu info
        if isfile('Resources\\Data\\cpu_family.json'):
            with open('Resources\\Data\\cpu_family.json', 'r') as file:
                self.cpu_family: dict = load(file)
        if isfile('Resources\\Data\\cpu_architecture.json'):
            with open('Resources\\Data\\cpu_architecture.json', 'r') as file:
                self.cpu_architecture: dict = load(file)
        # load ram info
        if isfile('Resources\\Data\\ram_type.json'):
            with open('Resources\\Data\\ram_type.json', 'r') as file:
                self.ram_type: dict = load(file)
        if isfile('Resources\\Data\\ram_form.json'):
            with open('Resources\\Data\\ram_form.json', 'r') as file:
                self.ram_form: dict = load(file)   

    def get_gpus(self: object) -> list:
        # get gpus info
        gpus: list = []
        for wmi_gpu in self.wmi_object.Win32_VideoController():
            for gpu in self.gpu_list:
                if gpu.name in wmi_gpu.Name:
                    gpus.append({'id': gpu.id, 'name': gpu.name, 'free_memory': int(gpu.memoryUsed), 'used_memory': int(gpu.memoryFree), 'total_memory': int(gpu.memoryTotal), 'temp': gpu.temperature, 'uuid': gpu.uuid, 'load': gpu.load*100, 'resolution': (wmi_gpu.CurrentHorizontalResolution, wmi_gpu.CurrentVerticalResolution), 'driver_version': gpu.driver, 'refresh_rate': wmi_gpu.CurrentRefreshRate, 'active_display': False if gpu.display_active == 'Disabled' else True})
        return gpus

    def get_cpus(self: object) -> dict:
        cpus: list = []
        for cpu in self.wmi_object.Win32_Processor():
            cpus.append({'name': cpu.Name, 'family': self.cpu_family[f'{cpu.Family}'], 'cores': cpu.NumberOfCores, 'threads': cpu.ThreadCount, 'clock_speed': cpu.CurrentClockSpeed, 'architecture': self.cpu_architecture[f'{cpu.Architecture}'], 'manufacturer': cpu.Manufacturer, 'description': cpu.Description})
        return cpus

    def get_rams(self: object) -> list:
        rams: list = []
        for memory in self.wmi_object.Win32_PhysicalMemory():
            rams.append({'manufacturer': memory.Manufacturer, 'capacity': int(memory.Capacity), 'speed': int(memory.Speed), 'type': self.ram_type[f'{memory.SMBIOSMemoryType}'], 'part_number': memory.PartNumber.strip(), 'serial': memory.SerialNumber, 'form_factor': self.ram_form[f'{memory.FormFactor}'], 'slot': memory.DeviceLocator, 'voltage': int(memory.ConfiguredVoltage), 'bank': memory.BankLabel})
        return rams

    def get_motherboard(self: object) -> dict:
        for motherboard in self.wmi_object.Win32_BaseBoard():
            print(motherboard)
        self.get_bios()
        return {'manufacturer': motherboard.Manufacturer, 'product': motherboard.Product, 'part_number': motherboard.SerialNumber, }
        

    
    def get_bios(self: object) -> None:
        for bios in self.wmi_object.Win32_BIOS():
            print(bios)

        # for bios in self.wmi_object.Win32_ComputerSystem():
        #     print(bios)
