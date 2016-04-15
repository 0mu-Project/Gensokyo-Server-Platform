# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app
from flask import request, render_template, Blueprint, url_for, redirect, session
from docker import Client
# index page main route page 
@app.route('/project')
def pview():
    return render_template('project.html')

@app.route('/docker')
def dockerview():
    if 'username' in session:
        cli = Client(base_url='unix://var/run/docker.sock')
        c = cli.containers(all=True)
        return render_template('docker.html', **locals())
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/run')
def run():
    if 'username' in session:
        clir = Client(base_url='unix://var/run/docker.sock')
        clirt = clir.create_container(tty=True, detach=True, image='0muproject/0mu-flask', name='0mu-Flask-06', ports=['8510', '22'], host_config=clir.create_host_config(port_bindings={
            8510: 8510,
            22: 2222
            })
            )
        clir.start(clirt.get('Id'))
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/stop/<Name>')
def dockerstop(Name):
    if 'username' in session:
        cli = Client(base_url='unix://var/run/docker.sock')
        cli.stop(container=Name)
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/start/<Name>')
def dockerstart(Name):
    if 'username' in session:
        cli = Client(base_url='unix://var/run/docker.sock')
        cli.start(container=Name)
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))
