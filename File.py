import os

class File:
    def __init__(self, fpath, fname):
        self.fpath = fpath
        self.fname = fname

    def size(self):
      return os.path.getsize(self.fpath)