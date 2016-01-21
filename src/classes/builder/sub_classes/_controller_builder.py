# -*- coding:utf-8 -*-

from ._package_builder import PackageBuilder
from ._helper_objects import ImportObj, ControllerObj
from ..app_recipe import *

''' this class create controller-layer. '''
class ControllerBuilder(PackageBuilder):

    def add_controller_init_file(self):
        imports = []
        blueprints = []
        for controller_recipe in controllers_recipe:
            controller_name = controller_recipe['name']
            from_name = '.' + controller_name + '_c'
            blueprint = controller_name+'_bp'
            import_names = [ blueprint ]
            import_obj = ImportObj(from_name, import_names=import_names)
            imports.append(import_obj)
            blueprints.append(blueprint)

        package_path = self.get_controller_path()
        self.add_init_file_to(package_path, imports=imports, blueprints=blueprints, rewrite=True)

        self.print_success('controller package created!')

    def add_controller_files(self):
        for controller_recipe in controllers_recipe:
            controller_name = controller_recipe['name']
            blueprint = controller_name+'_bp'
            url_prefix = None
            if 'url_prefix' in controller_recipe and controller_recipe['url_prefix']:
                url_prefix = controller_recipe['url_prefix']
            controller_obj = ControllerObj(controller_name, blueprint, url_prefix=url_prefix)
            self._add_controller_file(controller_name, controller_obj)

        self.print_success('controller files created!')

    def _add_controller_file(self, controller_name, controller_obj):
        src_file_path = self.get_controller_path() + '/' + controller_name + '_c.py'
        src_param = { 'controller_obj': controller_obj }
        src_content = self.get_rendered_src(tmpl_dir_controller+'/controller.tmpy', **src_param)
        self.add_file(src_file_path, src_content)

