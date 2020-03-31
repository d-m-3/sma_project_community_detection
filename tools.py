import time


class Timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        print(f"{self.message}")
        self.start = time.time()

    def __exit__(self, type, value, trace):
        time_ = time.time() - self.start
        print(f" - {time_:f} sec")
