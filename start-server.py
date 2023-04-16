from Server import Server
from ServerArguments import ServerArguments

arguments = ServerArguments()
args = arguments.parse()
host = args.host
port = args.port
storage_path = args.storage

server = Server(host, port, storage_path)
i = server.start()
while server.active:
    try:
        print('Para finalizar el server apretar q')
        if input().lower() == 'q':
            server.stop()
    except KeyboardInterrupt:
        server.stop()

