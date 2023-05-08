import paramiko
import sys
import os
import time
import getpass
from argparse import ArgumentParser
import pandas as pd
import threading

from utils import parse_manifest, setup_ssh, setup_node, setup_ssb
from experiments import hop_expirement

def main():
    parser = ArgumentParser()
    parser.add_argument("--manifest", help="manifest for cloudlab")
    parser.add_argument("--setup_node", help="whether to do node setup", default=False)

    args = parser.parse_args()
    nodes = parse_manifest(args.manifest)

    ssh_clients = {}
    intf_ips = {}
    for node in nodes:
        ssh_clients[node.name] = setup_ssh(node.username, node.hostname)
        intf_ips[node.name] = node.ips
        print(node.name)

    if args.setup_node:
        setup_node(ssh_clients, 'node_setup.sh')
    
    # run ssb-server and get their ids
    users = setup_ssb(ssh_clients, intf_ips)


    hop_expirement(users)


    for node in users:
        users[node].quit()
    

if __name__ == "__main__":
    main()