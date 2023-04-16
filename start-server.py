from Server import Server
from ServerArguments import ServerArguments

arguments = ServerArguments()
args = arguments.parse()
host = args.host
port = args.port
storage_path = args.storage

server = Server(host, port, storage_path)
server.start()