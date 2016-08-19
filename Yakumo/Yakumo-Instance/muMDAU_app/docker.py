# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app, socketio
from threading import Thread
from flask import render_template, url_for, redirect, session, request 
from docker import Client
pullthread = None
# index page main route page 
@app.route('/project')
def pview():
    return render_template('project.html')

@app.route('/docker')
def dockerview():
    if 'username' in session:
        cli = Client(base_url='tcp://'+ session['username'] +'.docker:14438')
        c = cli.containers(all=True)
        images = cli.images()
        return render_template('docker.html', **locals())
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/run')
def run():
    if 'username' in session:
        clir = Client(base_url='tcp://'+ session['username'] +'.docker:14438')
        clirt = clir.create_container(tty=True, detach=True, image='0muproject/0mu-flask', name='0mu-Flask-06', ports=['8510', '22'], host_config=clir.create_host_config(port_bindings={8510: 8510, 22: 2222}))
        clir.start(clirt.get('Id'))
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/stop/<Name>')
def dockerstop(Name):
    if 'username' in session:
        cli = Client(base_url='tcp://172.17.0.2:14458')
        cli.stop(container=Name)
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))

@app.route('/docker/start/<Name>')
def dockerstart(Name):
    if 'username' in session:
        return redirect(url_for('dockerview'))
    else:
        return redirect(url_for('main.index'))


@app.route('/docker/pull/<Name>', methods=['GET', 'POST'])
def dockerpull(Name):
    if request.method == 'POST':
        global pullthread
        if 'username' in session:
            pullthread = Thread(target=pull_connect(Name))
            pullthread.daemon = True
            pullthread.start()
            return '開始進行Pull'
        else:
            return redirect(url_for('main.index'))

def pull_connect(Name):
    cli = Client(base_url='tcp://172.17.0.2:14458')
    for line in cli.pull(Name, stream=True):
        socketio.emit('pull', {'info': eval(line.decode('utf-8')).get('status') + '</br>' +str(eval(line.decode('utf-8')).get('progress',''))}, namespace='/pull/info')
    socketio.emit('pull', {'info': "[Pull-Done] 請重新整理 Hakurei-Docker 界面"}, namespace='/pull/info')
