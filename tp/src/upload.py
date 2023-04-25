#!/usr/bin/env python3

from lib.Client import Client
from lib.ClientArguments import ClientArguments
from lib.Logging import Logging
from lib.OperationEnum import OperationEnum

arguments = ClientArguments(OperationEnum.UPLOAD)
args = arguments.parse()

host = args.host
port = args.port
fpath = args.filepath
fname = args.filename
verbose = args.verbose
transport_protocol = args.transport_protocol

log = Logging()
log.set_verbose(verbose)
client = Client(host, port)
status_operation = client.send_operation(OperationEnum.UPLOAD.value, fpath, fname)
if status_operation:
    connected = client.wait_confirmation()
    if not connected:
        client.close_socket()
        log.info('No obtuve respuesta del servidor, desconectando')
        exit(1)
    client.send_file(transport_protocol)
