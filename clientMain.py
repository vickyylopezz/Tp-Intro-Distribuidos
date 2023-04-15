import Client
import os
import sys
import argparse

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(mymodule_dir)

def parseArguments(parser):
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument('-v', '--verbose', dest='verbose',
                       required=False, help='increase output verbosity',
                       action='store_true')

    group.add_argument('-q', '--quiet', dest='verbose',
                       required=False, help='decrease output verbosity',
                       action='store_false')

    parser.set_defaults(verbose=False)

    parser.add_argument('-H', '--host', type=str, default='localhost',
                        required=False, help='server IP address', dest='addr')

    parser.add_argument('-p', '--port', type=int, default=8888,
                        required=False, help='server port')

    parser.add_argument('-s', '--src', type=str, default='./archivo',
                        required=True, help='source file path',
                        dest='filepath')

    parser.add_argument('-n', '--name', type=str, default='archivo',
                        required=False, help='file name', dest='filename')

parser = argparse.ArgumentParser(description='Envía un archivo al' +
                                    ' servidor para ser guardado' +
                                    ' con el nombre asignado')
parseArguments(parser)
args = parser.parse_args()

host = args.addr
port = args.port
fpath = args.filepath
fname = args.filename

client = Client.Client(host, port)
client.send(fpath, fname)
client.receive()