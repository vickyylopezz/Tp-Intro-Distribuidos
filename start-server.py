from Logging import Logging
from Server import Server
from ServerArguments import ServerArguments

arguments = ServerArguments()
args = arguments.parse()
host = args.host
port = args.port
storage_path = args.storage
verbose = args.verbose
transport_protocol = args.transport_protocol

log = Logging()
log.set_verbose(verbose)
server = Server(host, port, storage_path, transport_protocol)
server.start()
while server.active:
    try:
        log.info('Para finalizar q')
        if input().lower() == 'q':
            server.stop()
    except KeyboardInterrupt:
        server.stop()

