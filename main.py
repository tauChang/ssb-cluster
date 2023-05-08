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
    for node in nodes:
        ssh_clients[node.name] = setup_ssh(node.username, node.hostname)
        print(node.name)

    if args.setup_node:
        setup_node(ssh_clients, 'node_setup.sh')
    
    # run ssb-server and get their ids
    users = setup_ssb(ssh_clients)


    users["node-1"].follow(users["node-0"])
    users["node-2"].follow(users["node-0"])
    users["node-3"].follow(users["node-0"])
    users["node-4"].follow(users["node-0"])
    users["node-5"].follow(users["node-0"])
    hop_expirement(users)


    for node in users:
        users[node].quit()
    

if __name__ == "__main__":
    main()