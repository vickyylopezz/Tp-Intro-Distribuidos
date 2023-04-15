import Client
import os
import sys
import ClientArguments

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)

arguments = ClientArguments.ClientArguments()
args = arguments.parse()

host = args.addr
port = args.port
fpath = args.filepath
fname = args.filename

client = Client.Client(host, port)
client.send_operation(fpath, fname)
client.receive()
client.send_file()
