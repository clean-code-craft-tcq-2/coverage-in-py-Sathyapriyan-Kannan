class CoolingType:
    def __init__(self, lower_limit, upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit


passive = CoolingType(0, 35)
hi_active = CoolingType(0, 45)
med_active = CoolingType(0, 40)
