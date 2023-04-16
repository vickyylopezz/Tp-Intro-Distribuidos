#!/usr/bin/env python3

import Client
import ClientArguments
from OperationEnum import OperationEnum

arguments = ClientArguments.ClientArguments(OperationEnum.DOWNLOAD)
args = arguments.parse()

host = args.host
port = args.port
fpath = args.filepath
fname = args.filename

client = Client.Client(host, port)
client.send_operation("d", fpath, fname)
length, addr = client.receive()
client.send_confirmation(addr)
client.receive_file(length)
