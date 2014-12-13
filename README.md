BlueMarbleTileGenerator
=======================

Generates tiles from NASA's Blue Marble data


to run, do a git clone

```
git clone git@github.com:DanielCaldwell/BlueMarbleTileGenerator.git
```

install virtual box and vagrant

https://www.virtualbox.org/
https://www.vagrantup.com/

run vagrant to create a new virtual machine (vm is based off of ubuntu)

```
vagrant up
```

ssh to the virtual machine

```
vagrant ssh
```

once in the vagrant machine install the needed dependencies

```
/vagrant/install.sh
```

You cannot run the software in the /vagrant directory as vips throws an error. So run it from your local direcotry.

```
cd ~
cp /vagrant/*.py .
./run.py
```

If you want to change the month you are retriving or the tiles, do a quick edit of the run file. 



