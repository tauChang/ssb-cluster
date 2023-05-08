import threading
import paramiko
import sys
import os
import time

import xml.etree.ElementTree as ET

from collections import namedtuple
from user import User

Node = namedtuple('Node', ['name', 'hostname', 'username'])

def parse_manifest(manifest):
    tree = ET.parse(manifest)
    root = tree.getroot()

    # is this subject to change?
    nsmap = {'ns': 'http://www.geni.net/resources/rspec/3'}

    details = []

    for node in root.findall('ns:node', nsmap):
        name = node.get('client_id')
        auth = node.find('ns:services', nsmap).find('ns:login', nsmap)
        hostname = auth.get('hostname')
        username = auth.get('username')
        details.append(Node(name=name, hostname=hostname, username=username))

    return details

def setup_ssh(username: str, host: str):
    home_dir = os.path.expanduser('~')
    sshkey_fname = f'{home_dir}/.ssh/id_rsa'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connect {username}@{host}')
    # test ssh connection
    client.connect(hostname=host, username=username, key_filename=sshkey_fname)
    return client


def setup_node(ssh_clients, setup_script):
    def run_command(client, command):
        print(f'Running command {command}')
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return

    threads = []
    for name, client in ssh_clients.items():
        sftp = client.open_sftp()
        sftp.put(setup_script, 'node_setup.sh')
        sftp.close()
        # run node_setup.sh
        command = 'chmod +x node_setup.sh && bash node_setup.sh'
        thread = threading.Thread(target=run_command, args=(client, command))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def setup_ssb(ssh_clients):
    users = {}
    for name, client in ssh_clients.items():
        transport = client.get_transport()
        channel = transport.open_session()
        channel.exec_command("kill -9 $(ps -ef | grep '/usr/bin/ssb-server start' | grep -v grep | awk '{print $2}')")

        channel = transport.open_session()
        channel.exec_command("ssb-server start > /dev/null 2>&1")
        
        # sleep
        print(name)
        time.sleep(0.5)
        stdin, stdout, stderr = client.exec_command("ssb-server whoami")
        print(stderr.read().decode('utf-8'))    
        ssb_id = stdout.read().decode('utf-8').split(':')[1].strip().strip('"}').strip("\"\n")
        users[name] = User(name, client, ssb_id)
    return users