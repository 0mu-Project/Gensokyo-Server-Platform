# -*- coding: utf-8 -*-

from muMDAU_app import app 
from flask import session, redirect, url_for, request
import hashlib
from dbmongo import User
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['buser']
        passd = request.form['bpass']
        password = User.login(user)
        print(password)

        if not password:
            return '帳號錯誤'
        else:
            if password == passd:
                session['username'] = user
                return redirect(url_for('main.index'))
            else:
                return '密碼錯誤'

    else:
        return redirect(url_for('main.index'))
