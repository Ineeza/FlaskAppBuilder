# -*- coding:utf-8 -*-

from ._file_maker import FileMaker
from ..app_recipe import *

''' this class create each __init__ and wsgi files. '''
class PackageBuilder(FileMaker):

    def make_app_package(self):
        self.add_dir(self.get_controller_path())
        self.add_dir(self.get_model_path())
        self.add_dir(self.get_table_path())
        self.add_dir(self.get_dao_path())
        self.add_dir(self.get_service_path())

        self.print_success('app directory created!')

    def add_wsgi_file(self, rewrite=True):
        src_file_path = self.src_path + '/app.wsgi'

        wsgi_project_root = ON_MASTER_PROJECT_ROOT + '/' + self.src_dir_name
        wsgi_vertual_env = ON_MASTER_VIRTUAL_ENV

        src_param = { 'wsgi_project_root': wsgi_project_root, 'wsgi_vertual_env': wsgi_vertual_env }
        src_content = self.get_rendered_src(tmpl_dir_setting+'/app.wsgi.tmpy', **src_param)
        self.add_file(src_file_path, src_content, rewrite=rewrite)

        self.print_success('wsgi file created!')

    def add_init_file_to(self, package_path, imports=None, blueprints=None, rewrite=False):
        src_file_path = package_path + '/__init__.py'
        src_param = { 'imports': imports, 'blueprints': blueprints }
        src_content = self.get_rendered_src(tmpl_dir_init+'/__init__.tmpy', **src_param)
        self.add_file(src_file_path, src_content, rewrite=rewrite)
