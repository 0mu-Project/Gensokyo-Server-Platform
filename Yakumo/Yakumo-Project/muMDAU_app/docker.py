# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app
from flask import request, render_template, Blueprint, url_for, redirect, session
# index page main route page 
@app.route('/docker')
def ssh():
    if 'username' in session:
        return render_template('docker.html')
    else:
        return redirect(url_for('main.index'))
