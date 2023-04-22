import os
import logging

import xml.etree.ElementTree as ET

from collections import namedtuple
from argparse import ArgumentParser
import pandas as pd

Node = namedtuple('Node', ['name', 'intf_ip', 'host_ip', 'hostname', 'username'])

def parse_manifest(manifest):
    tree = ET.parse(manifest)
    root = tree.getroot()

    # is this subject to change?
    nsmap = {'ns': 'http://www.geni.net/resources/rspec/3'}

    details = []

    for node in root.findall('ns:node', nsmap):
        name = node.get('client_id')
        intf_ip = node.find('ns:interface', nsmap).find('ns:ip', nsmap).get('address')
        host_ip = node.find('ns:host', nsmap).get('ipv4')
        auth = node.find('ns:services', nsmap).find('ns:login', nsmap)
        hostname = auth.get('hostname')
        port = auth.get('port')
        username = auth.get('username')
        details.append(Node(name=name, intf_ip=intf_ip, host_ip=host_ip, hostname=hostname, username=username))

    return details

def create_config(details):
    config = pd.DataFrame(columns=details[0]._fields)

    for node_info in details:
        d = node_info._asdict()
        config = pd.concat([config, pd.DataFrame(d, index=[0])], ignore_index=True)
    
    return config

def main():
    logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser()
    parser.add_argument("--manifest", help="manifest for cloudlab")
    parser.add_argument("--output", help="output file", default="config.csv")

    args = parser.parse_args()
    details = parse_manifest(args.manifest)
    # note that here we are using the raft port and db port for all nodes
    file_path = args.output

    print(details)
    logging.info('Discovered N={} Nodes: {}'.format(len(details), details))

    config = create_config(details)
    config.to_csv(file_path, index=False)


if __name__ == '__main__':
    main()