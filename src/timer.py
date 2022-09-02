from time import time


class Timer:

    def __init__(self, interval=600):
        self.__start_time = 0
        self.interval = interval

    def __time_as_int(self):
        return int(round(time()))

    def start(self):
        self.__start_time = self.__time_as_int()

    def stop(self):
        self.__start_time = 0

    def check_interval(self):
        if self.__start_time:
            return self.interval <= (self.__time_as_int() - self.__start_time)
        else:
            return False

    def check(self):
        return self.__time_as_int() - self.__start_time
