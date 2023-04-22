import paramiko
import sys
import os
import time
import getpass
from argparse import ArgumentParser
import pandas as pd

from utils import parse_manifest, setup_ssh, setup_node, setup_ssb

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

    users["node0"].follow(users["node1"])
    users["node1"].follow(users["node0"])
    blobId = users["node0"].publishBlob("file1", 100)
    users["node1"].createLogStream()
    users["node1"].wantsBlob(blobId)
    users["node1"].getsBlob(blobId)
    users["node0"].whoami()
    users["node0"].quit()
    users["node1"].quit()
    # users["node0"].quit()
    

if __name__ == "__main__":
    main()