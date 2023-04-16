#!/usr/bin/env python3

import Client
import ClientArguments
from OperationEnum import OperationEnum

arguments = ClientArguments.ClientArguments(OperationEnum.UPLOAD)
args = arguments.parse()

host = args.host
port = args.port
fpath = args.filepath
fname = args.filename

client = Client.Client(host, port)
client.send_operation(OperationEnum.UPLOAD.value, fpath, fname)
client.receive()
client.send_file()
