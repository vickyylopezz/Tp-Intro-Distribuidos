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

log = Logging()
log.set_verbose(verbose)
log.set_entity('download')

client = Client.Client(host, port)
client.send_operation("d", fpath, fname)
length = client.receive_length()
if length == 0:
  client.close_socket()
  # log.log('No obtuve respuesta del servidor, desconectando')
  print('No obtuve respuesta del servidor, desconectando')
  exit(1)
client.send_confirmation()
client.receive_file(length)
