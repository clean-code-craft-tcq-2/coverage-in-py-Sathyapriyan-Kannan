class CoolingType:
    def __init__(self, lower_limit, upper_limit):
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit

    @property
    def lower_limit(self):
        return self.__lower_limit

    @property
    def upper_limit(self):
        return self.__upper_limit


passive = CoolingType(0, 35)
hi_active = CoolingType(0, 45)
med_active = CoolingType(0, 40)
