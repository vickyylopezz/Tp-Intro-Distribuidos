from Server import Server
from ServerArguments import ServerArguments

arguments = ServerArguments()
args = arguments.parse()
host = args.host
port = args.port
storage_path = args.storage
transport_protocol = args.transport_protocol

server = Server(host, port, storage_path, transport_protocol)
server.start()
while server.active:
    try:
        print('Para finalizar q')
        if input().lower() == 'q':
            server.stop()
    except KeyboardInterrupt:
        server.stop()

