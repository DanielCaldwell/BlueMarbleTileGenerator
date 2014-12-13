
# install dependencies
sudo apt-get -y install libvips
sudo apt-get -y install libvips-tools

sudo apt-get -y install python
sudo apt-get -y install python-dev
sudo apt-get -y install python-vipscc
sudo apt-get -y install python-virtualenv

# install other libraries into the virtual environment
sudo pip install -r requirements.txt
