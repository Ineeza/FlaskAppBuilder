# -*- coding:utf-8 -*-

'''
controller:
    { 'name': 'hoge' } => hoge_c.py, hoge_bp
    { 'name': 'api', 'url_prefix': '/apis' } => api_c.py, api_bp, url_prefix:/apis
'''
controllers_recipe = [  ]

'''
model_service: 'huga' => huga_service.py, HugaService
'''
model_services_recipe = [  ]


DB_TYPE = 'mysql'
DB_OPTION = '?charset=utf8'

DB_DEV_USER = ''   # root
# such DB_DEV_PASS should not be in this file. pass-input will be required in app-build.
DB_DEV_HOST = ''   # localhost
DB_DEV_SCHEME = '' # scheme

DB_MASTER_USER = ''
DB_MASTER_PASS = ''
DB_MASTER_HOST = ''
DB_MASTER_SCHEME = ''

ON_MASTER_PROJECT_ROOT = '' # /var/www/httpdocs/__projname__ etc.
ON_MASTER_VIRTUAL_ENV =  '' # /usr/lib/python2.6/site-packages


tmpl_dir_init = '_init'
tmpl_dir_config = '_config'
tmpl_dir_setting = '_setting'

tmpl_dir_controller = 'controller'
tmpl_dir_table = 'table'
tmpl_dir_dao = 'dao'
tmpl_dir_service = 'service'
