import os

from FileNotFoundException import FileNotFoundException


class File:
    def __init__(self, fpath, fname):
        self.fpath = fpath
        self.fname = fname
        self.fd = None

    def check(self):
        if not os.path.isfile(self.fpath):
            raise FileNotFoundException()

    def size(self):
        return os.path.getsize(self.fpath)

    def open(self, mode):
        self.fd = open(self.fpath, mode)

    def close(self):
        self.fd.close()

    def write(self, data):
        self.fd.write(data)

    def read(self, size):
        return self.fd.read(size)
