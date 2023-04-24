import Arguments
from OperationEnum import OperationEnum


class ClientArguments(Arguments.Arguments):
    def __init__(self, operation: OperationEnum):
        self.operation = operation
        super().__init__()

    def config(self):
        super().config()
        self.parser.add_argument(
            "-H",
            "--host",
            type=str,
            default="10.0.0.1",
            required=False,
            help="server IP address",
            dest="host",
        )
        self.parser.add_argument(
            "-p", "--port", type=int, default=8888, required=False, help="server port"
        )
        if self.operation == OperationEnum.UPLOAD:
            default_name = "new_file.txt"
            self.parser.add_argument(
                "-s",
                "--src",
                type=str,
                default="./files/file.txt",
                required=False,
                help="source file path",
                dest="filepath",
            )
        elif self.operation == OperationEnum.DOWNLOAD:
            default_name = "./files/file.txt"
            self.parser.add_argument(
                "-d",
                "--dst",
                type=str,
                default="new_file.txt",
                required=False,
                help="destination file path",
                dest="filepath",
            )

        self.parser.add_argument(
            "-n",
            "--name",
            type=str,
            default=default_name,
            required=False,
            help="file name",
            dest="filename",
        )
