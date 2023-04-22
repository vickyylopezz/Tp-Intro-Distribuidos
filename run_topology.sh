#!/bin/sh
number_of_hosts=$(($1+1))
sudo mn --custom ./topology.py --topo customTopo,loss=20,hosts=$number_of_hosts --mac -x