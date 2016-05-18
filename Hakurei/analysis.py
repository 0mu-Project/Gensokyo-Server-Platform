#!/usr/bin/env python
import sys, os
import configparser
import subprocess
hqsconfig = configparser.RawConfigParser()
hqsconfig.read(str(sys.argv[1]) + '/.hqsrc')

rqHost = None
rqEntry = None
pyEnv = None
pyPack = None

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def db_check():
    dbinsideval = None
    dboutsideval = None
    try:
        dbinside = hqsconfig.items('Extension-DB')
        dbinsideval = True
    except:
        dbinsideval = False
        pass
    try:
        dboutside = hqsconfig.items('Standalone-DB')
        dboutsideval = True
    except:
        pass
    if dbinsideval == dboutsideval:
        print(bcolors.FAIL + '[E] Can not have two DB Value !' + bcolors.ENDC)
        sys.exit()
    elif dbinsideval is False and dboutsideval is None:
        print(bcolors.WARNING + '[W] Dont have DB setting !' + bcolors.ENDC)


def require_check():
    global rqHost
    global rqEntry
    try:
        rqHost = hqsconfig.get('Require-Env', 'Host')
        rqEntry = hqsconfig.get('Require-Env', 'Entrypoint')
    except:
        print(bcolors.FAIL + '[E] RequireSection NotFound !' + bcolors.ENDC)
        sys.exit()

def pyenv_check():
    global pyEnv
    global pyPack
    try:
        pyEnv = hqsconfig.get('Python-Env', 'Env')
        pyPack = hqsconfig.get('Python-Env', 'Pack')
    except:
        print(bcolors.FAIL + '[E] PythonSection NotFound !' + bcolors.ENDC)
        sys.exit()

def GenDfile():
    if not os.path.exists('./DFile/'+ str(sys.argv[1])):
        subprocess.call('mkdir ./DFile/'+ str(sys.argv[1]),shell=True)
    subprocess.call('rm ./DFile/'+ str(sys.argv[1])+'/Dockerfile',shell=True)
    DFile = open( './DFile/'+ str(sys.argv[1]) + '/Dockerfile' , 'a')
    DFile.write('FROM HQSPack/Python:latest\nEXPOSE 80\n')
    DFile.write('CMD [\''+ pyEnv +' '+rqEntry + '\']')


if __name__ == '__main__':
    require_check()
    pyenv_check()
    db_check()
    print(pyEnv+' '+rqEntry) 
    GenDfile()
