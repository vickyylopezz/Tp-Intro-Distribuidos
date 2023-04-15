import Arguments


class ServerArguments(Arguments.Arguments):
    def __init__(self):
        super().__init__('<command description>')

    def config(self):
        super().config()
        self.parser.add_argument('-H', '--host', help='host service IP address',
                                 dest="addr", default='localhost', metavar='ADDR')
        self.parser.add_argument('-p', '--port', help='service port',
                                 default=8888, metavar='PORT', type=int)
        self.parser.add_argument('-s', '--storage', help='storage dir path',
                                 default="data_base", metavar='DIRPATH')
