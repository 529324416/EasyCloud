import time


class Timer:

    def __init__(self,interval):

        self.time = [time.time(),0]
        self.interval = interval

    def tick(self):

        self.time[1] = time.time()
        if self.time[1] - self.time[0] >= self.interval:
            self.time[0] = self.time[1]
            return True
        return False



