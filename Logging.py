import datetime


class LoggingMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logging(metaclass=LoggingMeta):
    def __init__(self):
        self.verbose = False
        self.entity = None

    def set_verbose(self, verbose):
        self.verbose = verbose

    def set_entity(self, entity):
        self.entity = entity

    def log(self, message):
        if self.verbose:
            now = datetime.datetime.now()
            print("{} - {} : {}".format(now, self.entity, message))
