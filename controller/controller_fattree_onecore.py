#! /usr/bin/python3

# ./controller/controller_fattree_onecore.py [k]
#   Insert P4 table entries to route traffic among hosts for FatTree topology
#   with [k] value

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
import sys

# Usage function


def usage():
    print(
        "Usage: ./controller/controller_fattree_onecore.py [k]\n\tInsert P4 table entries to route traffic among hosts for FatTree topology with [k] value")


class RoutingController(object):

    def __init__(self):
        self.topo = None
        try:
            self.topo = load_topo("topology.json")
        except Exception as e:
            print("Failed to open the topology database file 'topology.json'. Do you run the network with 'p4run'?\n\tCause: {}".format(e))
            exit(1)
        self.controllers = {}
        self.init()

    def init(self):
        self.connect_to_switches()
        self.reset_states()
        self.set_table_defaults()

    def connect_to_switches(self):
        for p4switch in self.topo.get_p4switches():
            thrift_port = self.topo.get_thrift_port(p4switch)
            self.controllers[p4switch] = SimpleSwitchThriftAPI(thrift_port)

    def reset_states(self):
        [controller.reset_state() for controller in self.controllers.values()]

    def set_table_defaults(self):
        for controller in self.controllers.values():
            controller.table_set_default("dmac", "drop", [])

    def route(self):
        k = 4
        try:
            k = int(sys.argv[1])
        except Exception as e:
            print("Failed to parse the argument [k]! Cause: {}".format(e))
            usage()
            exit(1)
        half_k = k // 2
        host_num = k * k * k // 4
        tor_num = k * k // 2
        agg_num = k * k // 2
        core_num = k * k // 4

        for sw_name, controller in self.controllers.items():
            # TODO: forwarding rules for all switches

            pass

    def main(self):
        self.route()


if __name__ == "__main__":
    controller = RoutingController().main()
