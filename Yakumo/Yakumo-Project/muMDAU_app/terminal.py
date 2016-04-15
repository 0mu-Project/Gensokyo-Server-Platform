# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from muMDAU_app import app
from threading import Thread
from flask import request, render_template, Blueprint, url_for, redirect, session
from database import ManageSQL, LoginSQL
import subprocess, os
from subprocess import PIPE
from time import sleep
main = Blueprint('main', __name__)
thread = None
# index page main route page 
@app.route('/terminal', methods=['GET', 'POST'])
def ssh():
    if 'username' in session:
        return render_template('index.html', **locals())
    else:
        return render_template('login.html')
