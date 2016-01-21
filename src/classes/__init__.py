# -*- coding:utf-8 -*-

from flask import Flask, session, g, render_template, request

app = Flask(__name__)
try:
    app.config.from_object('webconfig')
except:
    pass

#from flask.ext.cache import Cache
#app.config['CACHE_TYPE'] = 'simple'
#app.cache = Cache(app)

try:
    from classes.controller import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
except:
    print 'error on register-blueprint. check classes.__init__.'
    pass
