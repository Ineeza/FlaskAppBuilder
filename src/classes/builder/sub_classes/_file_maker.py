# -*- coding:utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader

from ..app_constants import *

PRINT_COLOR_RED = '\033[91m'
PRINT_COLOR_GREEN = '\033[92m'
PRINT_COLOR_END = '\033[0m'

class FileMaker(object):

    src_dir_name = None
    src_path = None
    builder_path = None
    tmpl_path = None
    jinja_env = None

    def __init__(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        self.src_dir_name = const_src_dir
        self.src_path = self.get_path_of_dir(current_path, const_src_dir)
        self.builder_path = self.get_path_of_dir(current_path, const_builder_dir)
        self.tmpl_path = self.builder_path + '/' + const_src_tmpl_dir
        self.jinja_env = Environment(loader=FileSystemLoader(self.tmpl_path, encoding='utf8'), autoescape=True)

    def add_dir(self, dir_path):
        if not self.exist_dir(dir_path):
            os.mkdir(dir_path)

    def add_file(self, file_path, file_content, rewrite=False):
        if self.exist_file(file_path) and not rewrite:
            pass
        else:
            f = open(file_path, 'w')
            f.write(file_content)
            f.close()

    def exist_dir(self, file_path):
        if os.path.exists(file_path) and os.path.isdir(file_path):
            return True
        else:
            return False

    def exist_file(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return True
        else:
            return False

    def get_rendered_src(self, template_path, **args):
        return self.jinja_env.get_template(template_path).render(args)

    def get_path_of_dir(self, target_path, target_dir):
        _dir = os.path.basename(target_path)
        if _dir == target_dir:
            return target_path
        parent_path = os.path.dirname(target_path)
        if len(parent_path) < 8:
            return None
        return self.get_path_of_dir(parent_path, target_dir)

    def get_controller_path(self):
        return self.get_src_file_path(const_controller_dir)

    def get_model_path(self):
        return self.get_src_file_path(const_model_dir)

    def get_table_path(self):
        return self.get_src_file_path(const_table_dir)

    def get_dao_path(self):
        return self.get_src_file_path(const_dao_dir)

    def get_service_path(self):
        return self.get_src_file_path(const_service_dir)

    def get_src_file_path(self, target_dir):
        return self.src_path + self._get_file_path_from_src('', const_src_file_json, target_dir)

    def _get_file_path_from_src(self, base_path, sub_dir_list, target_dir):
        for sub_dir in sub_dir_list:
            dir_name = sub_dir['dir']
            dir_subtree = sub_dir['subtree']
            current_path = base_path+'/'+dir_name
            if dir_name == target_dir:
                return current_path
            if dir_subtree:
                return self._get_file_path_from_src(current_path, dir_subtree, target_dir)
        return None

    def print_success(self, success_string):
        print(PRINT_COLOR_GREEN + success_string + PRINT_COLOR_END)

    def print_error(self, error_string):
        print(PRINT_COLOR_RED + error_string + PRINT_COLOR_END)

    def pascalize_string(self, target_str):
        return target_str.title().replace('_', '')

