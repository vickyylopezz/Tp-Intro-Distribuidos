import Arguments


class ClientArguments(Arguments.Arguments):
    def __init__(self):
        super().__init__('Envia un archivo al servidor para ser guardado con el nombre asignado')

    def config(self):
        super().config()
        self.parser.add_argument('-H', '--host', type=str, default='localhost',
                                 required=False, help='server IP address', dest='addr')
        self.parser.add_argument('-p', '--port', type=int, default=8888,
                                 required=False, help='server port')
        self.parser.add_argument('-s', '--src', type=str, default='./archivo',
                                 required=True, help='source file path',
                                 dest='filepath')
        self.parser.add_argument('-n', '--name', type=str, default='archivo',
                                 required=False, help='file name', dest='filename')
