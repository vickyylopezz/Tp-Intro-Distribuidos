import argparse


class Arguments:
    def __init__(self, description=None):
        self.parser = argparse.ArgumentParser(
            description=description or "< command description >"
        )
        self.config()

    def config(self):
        group = self.parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            required=False,
            help="increase output verbosity",
            action="store_true",
        )
        group.add_argument(
            "-q",
            "--quiet",
            dest="verbose",
            required=False,
            help="decrease output verbosity",
            action="store_false",
        )
        self.parser.set_defaults(verbose=False)

        transport_protocol = self.parser.add_mutually_exclusive_group(required=True)

        transport_protocol.add_argument(
            "-w",
            "--saw",
            const="saw",
            required=False,
            help="send file over UDP protocol" + "(Stop-and-Wait)",
            dest="transport_protocol",
            action="store_const",
        )

        transport_protocol.add_argument(
            "-r",
            "--sr",
            const="sr",
            required=False,
            help="send file over UDP protocol" + "(Selective Repeat)",
            dest="transport_protocol",
            action="store_const",
        )

    def parse(self):
        return self.parser.parse_args()
