#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0muMDAU Server
from muMDAU_app import app, socketio 
import sys, os, setting, logging
from database import InitDB
from muMDAU_app.index import main
from muMDAU_app.editor import peditor
from muMDAU_app.editor import markdown
# muMDAU_app setting
app.secret_key = setting.yourkey
app.register_blueprint(peditor, url_prefix='/edit')
app.register_blueprint(markdown, url_prefix='/md')
app.register_blueprint(main)
# Main function of MDAUServer
if __name__ == '__main__':
    # log writeing
    if os.geteuid() == 0:
        print('Yakumo is run on ' + str(setting.host) + ':' + str(setting.port))
    # check debug
        if setting.debug == 0:
            debugB = False 
            socketio.run(app, debug=debugB, host=str(setting.host), port=setting.port)
        else:
            debugB = True
            logging.basicConfig(filename=setting.s_log, level=logging.WARNING)
            logdebug = open(setting.s_log, 'w')
            print('!!!Important : Now is in debug mode.')
            socketio.run(app, debug=debugB, log=logdebug, host=str(setting.host), port=setting.port)
    else:
        sys.exit('Yakumo Admin must run as root')
         
