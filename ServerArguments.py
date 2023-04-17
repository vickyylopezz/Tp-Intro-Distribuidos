import Arguments


class ServerArguments(Arguments.Arguments):
    def __init__(self):
        super().__init__('<command description>')

    def config(self):
        super().config()
        self.parser.add_argument('-H', '--host', help='host service IP address',
                                 dest='host', default='10.0.0.1')
        self.parser.add_argument('-p', '--port', help='service port',
                                 dest='port', default=8888, type=int)
        self.parser.add_argument('-s', '--storage', help='storage dir path',
                                 dest='storage', default='./files')
