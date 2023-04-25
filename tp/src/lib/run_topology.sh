#!/bin/sh
number_of_hosts=$(($1+1))
loss=$2
sudo mn --custom ../topology.py --topo customTopo,loss=$loss,hosts=$number_of_hosts --mac -x