#!/usr/bin/env python3

from Client import Client
from ClientArguments import ClientArguments
from OperationEnum import OperationEnum

arguments = ClientArguments(OperationEnum.UPLOAD)
args = arguments.parse()

host = args.host
port = args.port
fpath = args.filepath
fname = args.filename

client = Client(host, port)
client.send_operation(OperationEnum.UPLOAD.value, fpath, fname)
client.receive()
client.send_file()
