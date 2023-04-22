import json

class User:
    def __init__(self, name, ssh_client, ssb_id):
        self.name = name
        self.ssh_client = ssh_client
        self.ssb_id = ssb_id
        self.friends = {self.ssb_id: self.name}
    
    def whoami(self):
        stdin, stdout, stderr = self.ssh_client.exec_command("ssb-server whoami")
        ssb_id = stdout.read().decode('utf-8').split(':')[1].strip().strip('"}').strip("\"\n")
        print(f"User {self.name} whoami {ssb_id}")

    def follow(self, user):
        self.ssh_client.exec_command(f"ssb-server publish --type contact --contact {user.ssb_id} --following")
        print(f"User {self.name} is following {user.name}")
        self.friends[user.ssb_id] = user.name

    def unfollow(self, user):
        self.ssh_client.exec_command(f"ssb-server publish --type contact --contact {user.ssb_id} --no-following")
        print(f"User {self.name} is unfollowing {user.name}")
        del self.friends[user.ssb_id]

    def post(self, text):
        self.ssh_client.exec_command(f"ssb-server publish --type post --text {text}")
        print(f"User {self.name} posted {text}")

    def publishBlob(self, filename, bytes):
        # create a file that has bytes size
        # add blob
        # post about blob
        _, _, _ = self.ssh_client.exec_command(f"dd if=/dev/urandom of={filename} bs=1 count={bytes}")
        stdin, stdout, stderr = self.ssh_client.exec_command(f"cat {filename} | ssb-server blobs.add")
        blob_id = stdout.read().decode('utf-8').strip()
        print(f"User {self.name} added blob {blob_id}")

        cmd = "ssb-server publish --type post --text 'checkout this file!'"
        cmd += f" --mentions.link '{blob_id}'"
        # cmd += f" --mentions.name '{filename}'"
        # cmd += f" --mentions.size {bytes}"
        # cmd += f" --mentions.type 'text/plain'"
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        # print(stdout.read().decode('utf-8'))
        # print(stderr.read().decode('utf-8'))
        print(f"User {self.name} posted about blob {blob_id}")
        
        return blob_id
    
    def createLogStream(self):
        stdin, stdout, stderr = self.ssh_client.exec_command(f"ssb-server createLogStream")
        # print(stdout.read().decode('utf-8'))
        print(f"User {self.name} created log stream")
    
    def wantsBlob(self, blob_id):
        # execute command and print output
        stdin, stdout, stderr = self.ssh_client.exec_command(f"ssb-server blobs.want \"{blob_id}\"")
        # output = stdout.read().decode('utf-8')
        print(f"User {self.name} wants blob {blob_id}")
    
    def getsBlob(self, blob_id):
        stdin, stdout, stderr = self.ssh_client.exec_command(f"ssb-server blobs.get \"{blob_id}\"")
        # output = stdout.read().decode('utf-8')
        print(f"User {self.name} gets blob {blob_id}")

    def friendsHop(self):
        stdin, stdout, stderr = self.ssh_client.exec_command(f"ssb-server friends.hops")
        output_dict = json.loads(stdout.read().decode('utf-8'))
        print({self.friends[k]: v for k,v in output_dict.items()})

    def quit(self):
        # find the process id of ssb-server and kill
        stdin, stdout, stderr =self.ssh_client.exec_command("ps -ef | grep '/usr/bin/ssb-server start' | grep -v grep | awk '{print $2}'")
        pid = stdout.read().decode('utf-8').strip()
        self.ssh_client.exec_command(f"kill -9 {pid}")
        print(f"User {self.name} quit")
    
    def __str__(self):
        return f"User {self.name} with id {self.ssb_id}"