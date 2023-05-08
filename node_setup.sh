#!/bin/bash

# change shell to bash
sudo usermod -s /bin/bash $USER
rm -rf .ssb

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
sudo chown -R 20001:2544 "/users/tauchang/.npm"
sudo npm install -g npm@9.6.5
sudo npm install -g ssb-server
sudo npm install ssb-client
sudo npm install --save ssb-friends
sudo npm install --save ssb-replication-scheduler
sudo npm install --save ssb-ebt
sudo npm install --save ssb-db2
sudo npm install -g sodium-native
sudo npm audit fix --force

sudo apt install -y curl autotools-dev automake
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 10
nvm alias default 10
npm install -g node-gyp
npm install -g ssb-server
# code --install-extension GitHub.copilot