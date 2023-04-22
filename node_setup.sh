#!/bin/bash

# change shell to bash
sudo usermod -s /bin/bash $USER

# update gcc
yes '' | sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get -y update
sudo apt-get -y install gcc-9 g++-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-9

# update git
yes '' | sudo add-apt-repository ppa:git-core/ppa
sudo apt -y update
sudo apt -y install git

# install npm and nodejs
sudo apt -y update
sudo apt-get install -y build-essential
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - &&\
sudo apt-get install -y nodejs

# install ssb
sudo npm install -g npm@9.6.5
sudo npm install -g ssb-server
sudo npm install ssb-client
sudo npm install --save ssb-friends
sudo npm install --save ssb-replication-scheduler
sudo npm install --save ssb-ebt
sudo npm install --save ssb-db2
sudo npm install -g sodium-native
sudo npm audit fix --force

# code --install-extension GitHub.copilot