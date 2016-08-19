#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Server first time install py
import sys
import os
from subprocess import call 
def get_distribution():
    with open('/tmp/osver') as f:
        version = f.read().lower().split()[0]
        dicti = {'arch': lambda: 'pacman --noconfirm -Syu ', 
                 'debian': lambda: 'apt-get -y install ',
                 'ubuntu': lambda: 'apt-get -y install ',
                 'centos': lambda: 'yum -y install ',
                 'redhate': lambda: 'yum -y install ',
                 'fedora': lambda: 'dnf -y install '
                 }.get(version, lambda: 'Others ')()
    return dicti

def package_install():
    with open('/tmp/osver') as f:
        version = f.read().lower().split()[0]
        with open('./installer/pack/package_' + version + '.need') as pack:
            package = pack.read().lower()
            print(package)
            call([str(get_distribution()) + str(package)], shell=True)

# check version_info of python 
def checkpython():
    if sys.version_info[0] == 3:
        # if use pypy3 will have this sys builtin
        is_pypy = '__pypy__' in sys.builtin_module_names
        if is_pypy is True:
            try:
                import flask
                return 'pypy3'
            except ImportError:
                try:
                    import pip  # NOQA
                    print('You dont have flask install , Auto Install!')
                    print('Please enter root password !')
                    # call subprocess to install unfound modules
                    call(['sudo pypy3 -m pip install Flask'], shell=True)
                    call(['sudo pypy3 -m pip install six'], shell=True)
                except ImportError:
                    print('You dont have pip install , please input your password to install ')
                    call(['curl -s https://bootstrap.pypa.io/get-pip.py |sudo pypy3'], shell=True)
                return 'pypy3'
        else:
            try:
                import flask  # NOQA
                return 'python3'
            except ImportError:
                print('You dont have flask install , please input your password to install flask . ')
                # call subprocess to install unfound modules
                call(['sudo python3 -m pip install Flask'], shell=True)
                call(['sudo python3 -m pip install six'], shell=True)
                return 'python3'
    else:
        return 'python2'

def flask_installer():
    os.mkdir('/tmp/gensokyo')
    call(['git clone https://github.com/0mu-project/flask.git'], shell=True, cwd='/tmp/gensokyo')


# run master branch git pull to update server
def version_update():
    print('# Git status')
    call(['git pull'], shell=True)

def docker_preenv():
    call(['curl -sSL https://get.docker.com/ | sh'],shell=True)
    call(['docker network create --subnet=172.99.0.0/16 dns0'],shell=True)
    call(['docker run -it -d --name="dns" --hostname="dns" --net dns0 --ip 172.99.0.255 -v /var/run/docker.sock:/docker.sock phensley/docker-dns'],shell=True)
    call(['docker build ./Hakurei/hakurei-dind/'], shell=True)


# Main class 
if __name__ == '__main__':
    if not os.path.exists('/etc/gensokyo/install.lock'):
        if not os.geteuid() == 0:
            sys.exit('Installer must run as root')
        else:
            call(['head -n 1 /etc/os-release | sed -r \'s/NAME=//g\' | sed -r  \'s/"//g\'  > /tmp/osver'], shell=True)
            package_install()
    else:
        print('install.lock is aviable , please make sure installer is run or not.')
