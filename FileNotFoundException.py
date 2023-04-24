class FileNotFoundException(Exception):
    def __init__(self):
        super().__init__('File not found')
