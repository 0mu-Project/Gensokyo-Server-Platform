# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app, socketio
from threading import Thread
from flask import request, render_template, Blueprint, url_for, redirect, session
from database import ManageSQL, LoginSQL
import subprocess, os
from subprocess import PIPE
from time import sleep
main = Blueprint('main', __name__)
thread = None
# index page main route page 
@main.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        p = subprocess.Popen(['python3 ./muMDAU_app/pydeamon/cpuinfo.py core'], cwd='./', shell=True, stdout=PIPE, stderr=PIPE)
        core, errlog = p.communicate()
        global thread
        if thread is None:
            thread = Thread(target=info_connect)
            thread.daemon = True
            thread.start()
        return render_template('index.html', **locals())
    else:
        return render_template('login.html')


@app.route('/project')
def project():
    return render_template('project.html')


def info_connect():
    while True:
        p = subprocess.Popen(['python3 ./muMDAU_app/pydeamon/cpuinfo.py percent'], cwd='./', shell=True, stdout=PIPE, stderr=PIPE)
        cpupercent, cpuerrlog = p.communicate()
        m = subprocess.Popen(['python3 ./muMDAU_app/pydeamon/mem.py'], cwd='./', shell=True, stdout=PIPE, stderr=PIPE)
        mempercent, merrlog = m.communicate()
        ns = subprocess.Popen(['python3 ./muMDAU_app/pydeamon/net.py sent'], cwd='./', shell=True, stdout=PIPE, stderr=PIPE)
        nslog, nserrlog = ns.communicate()
        nr = subprocess.Popen(['python3 ./muMDAU_app/pydeamon/net.py recv'], cwd='./', shell=True, stdout=PIPE, stderr=PIPE)
        nrlog, nrerrlog = nr.communicate()
        socketio.emit('info', {'cpuusage': str(cpupercent.decode('utf-8')), 'mem': str(mempercent.decode('utf-8')), 'ns': str(nslog.decode('utf-8')), 'nr': str(nrlog.decode('utf-8'))}, namespace='/info')
        sleep(2)

@app.route('/info/sys/')
def isys():
    with open('/proc/uptime') as upfile:
        raw = upfile.read()
        fuptime = int(raw.split('.')[0])
        day = int(fuptime / 86400)
        fuptime = fuptime % 86400
        hour = int(fuptime / 3600)
        fuptime = fuptime % 3600
        minute = int(fuptime / 60)
        uptime = '{daystring}{hours}:{mins:02d}'.format(daystring='{days} day{s}, '.format(days=day, s=('s' if day > 1else '')) if day else '', hours=hour, mins=minute)
    upt = uptime
    hostname = 'Gensokyo.io'
    lavg = os.getloadavg()
    return render_template('info.html', **locals())


# init route to first time use
@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        import hashlib
        hashsha = hashlib.sha256(passd.replace('\n', '').encode())
        ManageSQL.addUser(user, hashsha.hexdigest(), '1', '0')
        return redirect(url_for('main.index'))
    else:
        return render_template('first.html')

# test of adduser route page 
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        user = request.form['buser']
        if LoginSQL.getPass(user) is None:
            import hashlib
            import random
            ans = random.uniform(1, 10)
            hashpass1 = hashlib.sha1(str(ans).encode())
            passd1 = hashpass1.hexdigest()
            hashpass0 = hashlib.sha256(passd1.replace('\n', '').encode())
            ManageSQL.addUser(user, hashpass0.hexdigest(), '0', '1')
            return passd1
        else:
            return '使用者已經他媽的存在了喔！'
