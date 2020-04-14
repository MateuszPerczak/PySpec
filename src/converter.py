class Convert:
    @staticmethod
    def BytesToMegabytes(size: int) -> str:
            return f"{round(float(float(size / 1024) / 1024), 3)} MB"

    @staticmethod
    def BytesToGigabytes(size: int) -> str:
        return f"{round(float(float(float(size / 1024) / 1024) / 1024), 3)} GB"
    
    @staticmethod
    def KilobytesToMegabytes(size: int) -> str:
        return f"{float(size / 1024)} MB" 

    # B = float(size * 8)
    # KB = float(B / 1024)
    # MB = float(KB / 1024) # 1,048,576
    # GB = float(MB / 1024) # 1,073,741,824
    # TB = float(GB / 1024) # 1,099,511,627,776