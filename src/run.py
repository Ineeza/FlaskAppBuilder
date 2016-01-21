# -*- coding:utf-8 -*-

import socket, sys
from classes import app
from classes.builder import AppBuilder

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        AppBuilder().init_app()
        sys.exit(0)

    if app.config['ON_MASTER']:
        app.run(host=app.config['MASTER_HOST'], port=80, debug=app.config['DEBUG'], use_debugger=app.config['USE_DEBUGGER'], use_reloader=False)
    else:
    	app.run(host=app.config['LOCAL_HOST'], debug=app.config['DEBUG'], use_debugger=app.config['USE_DEBUGGER'], use_reloader=False)

