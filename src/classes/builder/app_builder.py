# -*- coding:utf-8 -*-

from .sub_classes import ControllerBuilder, ModelBuilder

class AppBuilder(ControllerBuilder, ModelBuilder):

    def init_app(self):
        db_set = self.prepare_db_engine()
        if not db_set:
            self.print_error('to build app source code, confirm local db settings on app_recipe or password.')
            return

        self.make_app_package()
        self.add_wsgi_file()
        self.add_webconfig_files()
        self.add_model_setting_file()

        self.add_table_init_file()
        self.add_table_files()

        self.add_dao_init_file()
        self.add_dao_files()

        self.add_service_init_file()
        self.add_service_files()

        self.add_model_init_file()

        self.add_controller_init_file()
        self.add_controller_files()
