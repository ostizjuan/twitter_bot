from time import time


class Timer:

    def __init__(self, interval=600):
        self.__start_time = 0
        self.interval = interval

    def __time_as_int():
        return int(round(time.time() * 100))

    def start(self):
        self.__start_time = self.__time_as_int()

    def check_interval(self):
        if self.__start_time:
            if self.__interval >= (self.__time_as_int() - self.__start_time):
                self.__start_time = self.__time_as_int()
                return True
        else:
            return False
