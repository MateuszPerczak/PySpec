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
        try:
            # get gpus info
            gpus: list = []
            for wmi_gpu in self.wmi_object.Win32_VideoController():
                for gpu in self.gpu_list:
                    if gpu.name in wmi_gpu.Name:
                        gpus.append({'id': gpu.id, 'name': gpu.name, 'free_memory': int(gpu.memoryUsed), 'used_memory': int(gpu.memoryFree), 'total_memory': int(gpu.memoryTotal), 'temp': gpu.temperature, 'uuid': gpu.uuid, 'load': gpu.load*100, 'resolution': (wmi_gpu.CurrentHorizontalResolution, wmi_gpu.CurrentVerticalResolution), 'driver_version': gpu.driver, 'refresh_rate': wmi_gpu.CurrentRefreshRate, 'active_display': False if gpu.display_active == 'Disabled' else True})
            return gpus
        except Exception as _:
            return []

    def get_cpus(self: object) -> dict:
        try:
            cpus: list = []
            for cpu in self.wmi_object.Win32_Processor():
                cpus.append({'name': cpu.Name, 'family': self.cpu_family[f'{cpu.Family}'], 'cores': cpu.NumberOfCores, 'threads': cpu.ThreadCount, 'clock_speed': float(cpu.CurrentClockSpeed), 'architecture': self.cpu_architecture[f'{cpu.Architecture}'], 'manufacturer': cpu.Manufacturer, 'description': cpu.Description})
            return cpus
        except Exception as _:
            return []

    def get_rams(self: object) -> list:
        try:
            rams: list = []
            for memory in self.wmi_object.Win32_PhysicalMemory():
                rams.append({'manufacturer': memory.Manufacturer, 'capacity': int(memory.Capacity), 'speed': int(memory.Speed), 'type': self.ram_type[f'{memory.SMBIOSMemoryType}'], 'part_number': memory.PartNumber.strip(), 'serial': memory.SerialNumber, 'form_factor': self.ram_form[f'{memory.FormFactor}'], 'slot': memory.DeviceLocator, 'voltage': int(memory.ConfiguredVoltage), 'bank': memory.BankLabel})
            return rams
        except Exception as _:
            return []

    def get_motherboard(self: object) -> dict:
        try:
            chipset: object = None
            for device in self.wmi_object.Win32_PnPEntity(ClassGuid="{4d36e97d-e325-11ce-bfc1-08002be10318}"):
                if 'Chipset' in device.Caption:
                    chipset = device
            mem_cfg: object = self.wmi_object.Win32_PhysicalMemoryArray()[0]
            for motherboard in self.wmi_object.Win32_BaseBoard():
                return {'manufacturer': motherboard.Manufacturer, 'product': motherboard.Product, 'part_number': motherboard.SerialNumber, 'chipset': chipset.Caption, 'memory_slots': mem_cfg.MemoryDevices, 'max_capacity': int(mem_cfg.MaxCapacityEx)}
        except Exception as _:
            return {}

    def get_bios(self: object) -> list:
        try:
            bioses: list = []
            for bios in self.wmi_object.Win32_BIOS():
                bioses.append({'primary': bios.PrimaryBIOS, 'version': bios.SMBIOSBIOSVersion, 'manufacturer': bios.Manufacturer, 'release': f'{bios.ReleaseDate[6:8]}-{bios.ReleaseDate[4:6]}-{bios.ReleaseDate[0:4]}'})
            return bioses
        except Exception as _:
            return []

