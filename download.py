#!/usr/bin/env python3

import Client
import ClientArguments
from OperationEnum import OperationEnum
from Logging import Logging

arguments = ClientArguments.ClientArguments(OperationEnum.DOWNLOAD)
args = arguments.parse()

host = args.host
port = args.port
fpath = args.filepath
fname = args.filename
verbose = args.verbose
transport_protocol = args.transport_protocol

log = Logging()
log.set_verbose(verbose)

client = Client.Client(host, port)
client.send_operation("d", fpath, fname)
length = client.receive_length()
if int(length) == 0:
    client.close_socket()
    log.info('No obtuve respuesta del servidor, desconectando')
    exit(1)
elif int(length) == -1:
    client.close_socket()
    log.info('Archivo no encontrado')
    exit(1)
else:
    client.send_confirmation()
    client.receive_file(length, transport_protocol)
