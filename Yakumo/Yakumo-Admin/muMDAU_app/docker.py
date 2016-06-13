# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app
from flask import render_template, url_for, redirect, session 
from docker import Client
import subprocess
pullthread = None
# index page main route page 
@app.route('/project')
def pview():
    return render_template('project.html')

@app.route('/user')
def userview():
    if 'username' in session:
        cli = Client(base_url='unix://var/run/docker.sock')
        c = cli.containers(all=True)
        images = cli.images()
        return render_template('docker.html', **locals())
    else:
        return redirect(url_for('main.index'))

@app.route('/user/add/<Name>/<Mail>/<CPU>/<Mem>')
def run(Name, Mail, CPU, Mem):
    if 'username' in session:
        import hashlib
        import random
        ans = random.uniform(1, 10)
        hashpass = hashlib.sha1(str(ans).replace('\n', '').encode()).hexdigest()
        print(hashpass)
        subprocess.call('useradd ' + Name + ' -m -p ' + str(hashpass) + ' -s /bin/hshell', shell=True)
        subprocess.call('gpasswd -a ' + Name + ' docker', shell=True)
        clir = Client(base_url='unix://var/run/docker.sock')
        clirt = clir.create_container(hostname=str(Name + '-dind'), tty=True, detach=True, image='hakurei-dind', name=str(Name), cpu_shares=int(CPU), host_config=clir.create_host_config(mem_limit=str(Mem), privileged=True))
        clir.start(clirt.get('Id'))
        print(clirt.get('Id'))
        print(Mail)
        return redirect(url_for('userview'))
    else:
        return redirect(url_for('main.index'))
