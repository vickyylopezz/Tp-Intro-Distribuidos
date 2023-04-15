import Server
import argparse

def parseArguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose',
                       help='increase output verbosity', action='store_true')
    group.add_argument('-q', '--quiet', help='decrease output verbosity',
                       dest='verbose', action='store_false')

    parser.add_argument('-H', '--host', help='host service IP address',
                        dest="addr", default='localhost', metavar='ADDR')
    parser.add_argument('-p', '--port', help='service port',
                        default=8888, metavar='PORT', type=int)
    parser.add_argument('-s', '--storage', help='storage dir path',
                        default="data_base", metavar='DIRPATH')


parser = argparse.ArgumentParser(
    'start-server', description='<command description>')

parseArguments(parser)
args = parser.parse_args()
host = args.addr
port = args.port
storage_path = args.storage

server = Server.Server(host, port, storage_path)