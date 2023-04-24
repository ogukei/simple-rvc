
# https://github.com/w-okada/voice-changer/blob/08d07c599718a1395ae6a4d1eda71de1f8defd88/server/voice_changer/utils/Timer.py

import time

class Timer(object):
    def __init__(self, title: str):
        self.title = title

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *_):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
