import argparse


class Arguments:
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)
        self.config()

    def config(self):
        group = self.parser.add_mutually_exclusive_group(required=False)
        group.add_argument('-v', '--verbose', dest='verbose',
                           required=False, help='increase output verbosity',
                           action='store_true')
        group.add_argument('-q', '--quiet', dest='verbose',
                           required=False, help='decrease output verbosity',
                           action='store_false')
        self.parser.set_defaults(verbose=False)

    def parse(self):
        return self.parser.parse_args()
