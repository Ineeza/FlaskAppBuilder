# -*- coding:utf-8 -*-

import getpass
from sqlalchemy import create_engine, inspect

from ._package_builder import PackageBuilder
from ._helper_objects import column_type_string_dict, column_type_default_dict, \
    ImportObj, TableObj, ColumnObj, DaoObj, ServiceObj
from ..app_recipe import *

''' this class create model-layer[table,dao,service] and webconfig. '''
class ModelBuilder(PackageBuilder):

    alchemy_engine = None
    db_pass = None

    def prepare_db_engine(self):
        print 'input DB connection password for ' + DB_DEV_USER + ': '
        self.db_pass = getpass.getpass()
        db_url = '%(type)s://%(user)s:%(pass)s@%(host)s/%(scheme)s%(option)s' \
            % { 'type': DB_TYPE, 'user': DB_DEV_USER, 'pass': self.db_pass, \
                'host': DB_DEV_HOST, 'scheme': DB_DEV_SCHEME, 'option': DB_OPTION }
        try:
            self.alchemy_engine = create_engine(db_url)
            inspect(self.alchemy_engine) # for test conenction.
            return True
        except Exception as e:
            # print 'incorrect db connection.'
            return False

    def add_webconfig_files(self):
        src_file_path = self.src_path + '/webconfig.py'
        src_param = {}
        src_content = self.get_rendered_src(tmpl_dir_setting+'/webconfig.tmpy', **src_param)
        self.add_file(src_file_path, src_content)

        _src_file_path = self.src_path + '/webconfig_master.py'
        _src_param = { 'db_master_host': DB_MASTER_HOST, 'db_master_user': DB_MASTER_USER, \
                'db_master_pass': DB_MASTER_PASS, 'db_master_scheme': DB_MASTER_SCHEME }
        _src_content = self.get_rendered_src(tmpl_dir_setting+'/webconfig_master.tmpy', **_src_param)
        self.add_file(_src_file_path, _src_content)

        __src_file_path = self.src_path + '/webconfig_local.py'
        __src_param = { 'db_local_host': DB_DEV_HOST, 'db_local_user': DB_DEV_USER, \
                'db_local_pass': self.db_pass, 'db_local_scheme': DB_DEV_SCHEME }
        __src_content = self.get_rendered_src(tmpl_dir_setting+'/webconfig_local.tmpy', **__src_param)
        self.add_file(__src_file_path, __src_content)

        self.print_success('webconfig files created!')

    def add_model_setting_file(self):
        src_file_path = self.get_model_path() + '/_settings.py'
        src_param = {}
        src_content = self.get_rendered_src(tmpl_dir_setting+'/model_settings.tmpy', **src_param)
        self.add_file(src_file_path, src_content)

        self.print_success('model-settings file created!')

    def add_table_init_file(self):
        if not self.alchemy_engine:
            return
        imports = []
        inspector = inspect(self.alchemy_engine)
        for table_name in inspector.get_table_names():
            from_name = '.' + table_name
            import_names = [ self.pascalize_string(table_name) ]
            import_obj = ImportObj(from_name, import_names=import_names)
            imports.append(import_obj)

        package_path = self.get_table_path()
        self.add_init_file_to(package_path, imports=imports, rewrite=True)
        self.print_success('model-table package created!')

    def add_table_files(self):
        if not self.alchemy_engine:
            return
        inspector = inspect(self.alchemy_engine)
        for table_name in inspector.get_table_names():

            columns = []
            primary_keys = inspector.get_primary_keys(table_name)
            #indexes = inspector.get_indexes(table_name)
            for column in inspector.get_columns(table_name):
                # create column-obj for src-file creations.
                column_name = column['name']
                column_type = column['type'].__class__.__name__
                if column_type in column_type_string_dict:
                    column_type = column_type_string_dict[column_type]
                else:
                    #column_type = '__IMPLE__'
                    pass
                primary_key = False
                if column_name in primary_keys:
                    primary_key = True
                nullable = column['nullable']
                autoincrement = False
                if 'autoincrement' in column:
                    autoincrement = column['autoincrement']
                default = 'None'
                if column_type in column_type_default_dict:
                    default = column_type_default_dict[column_type]
                if 'default' in column and column['default']:
                    if column_type == 'BigInteger' or column_type == 'Integer':
                        default = column['default'].replace('\'', '')

                column_obj = ColumnObj(column_name, column_type, primary_key, nullable, autoincrement, default=default)
                columns.append(column_obj)
            table_class_name = self.pascalize_string(table_name)
            table_obj = TableObj(table_name, table_class_name, columns=columns)
            self._add_table_file(table_name, table_obj)
        self.print_success('model-table files created!')

    def add_dao_init_file(self):
        if not self.alchemy_engine:
            return
        imports = [ ImportObj('._dao', import_names=['DAO']) ]

        inspector = inspect(self.alchemy_engine)
        for table_name in inspector.get_table_names():
            from_name = '.' + table_name + '_dao'
            import_names = [ self.pascalize_string(table_name)+'DAO' ]
            import_obj = ImportObj(from_name, import_names=import_names)
            imports.append(import_obj)

        package_path = self.get_dao_path()
        self.add_init_file_to(package_path, imports=imports, rewrite=True)
        self.print_success('model-dao package created!')

    def add_dao_files(self):
        if not self.alchemy_engine:
            return

        self._add_dao_base_file()

        inspector = inspect(self.alchemy_engine)
        for table_name in inspector.get_table_names():

            columns = []
            primary_keys = inspector.get_primary_keys(table_name)
            #indexes = inspector.get_indexes(table_name)
            for column in inspector.get_columns(table_name):
                # create column-obj for src-file creations.
                column_name = column['name']
                column_type = column['type'].__class__.__name__
                if column_type in column_type_string_dict:
                    column_type = column_type_string_dict[column_type]
                else:
                    self.print_error('sorry, column-type ' + column_type + ' at ' + column_name + ' is not supported, in this builder.')
                autoincrement = False
                if 'autoincrement' in column:
                    autoincrement = column['autoincrement']
                default = 'None'
                if column_type in column_type_default_dict:
                    default = column_type_default_dict[column_type]
                if 'default' in column and column['default']:
                    if column_type == 'BigInteger' or column_type == 'Integer':
                        default = column['default'].replace('\'', '')

                # primary_key, nullable are not required for dao-file creations.
                column_obj = ColumnObj(column_name, column_type, False, False, autoincrement, default=default)
                columns.append(column_obj)
            table_class_name = self.pascalize_string(table_name)
            dao_class_name = table_class_name + 'DAO'
            dao_obj = DaoObj(table_name, table_class_name, dao_class_name, columns=columns, primary_keys=primary_keys)
            self._add_dao_file(table_name, dao_obj)
        self.print_success('model-dao files created!')

    def add_service_init_file(self):
        imports = []
        for model_service_name in model_services_recipe:
            from_name = '.' + model_service_name + '_service'
            import_names = [ self.pascalize_string(model_service_name)+'Service' ]
            import_obj = ImportObj(from_name, import_names=import_names)
            imports.append(import_obj)

        package_path = self.get_service_path()
        self.add_init_file_to(package_path, imports=imports, rewrite=True)
        self.print_success('model-service package created!')

    def add_service_files(self):
        for model_service_name in model_services_recipe:
            service_class_name = self.pascalize_string(model_service_name)+'Service' 
            service_obj = ServiceObj(service_class_name)
            self._add_service_file(model_service_name, service_obj)
        self.print_success('model-service files created!')

    def add_model_init_file(self):
        import_names = []
        from_name = '.service'
        for model_service_name in model_services_recipe:
            import_name = self.pascalize_string(model_service_name)+'Service'
            import_names.append(import_name)
        imports = [ ImportObj(from_name, import_names=import_names) ]

        package_path = self.get_model_path()
        self.add_init_file_to(package_path, imports=imports, rewrite=True)
        self.print_success('model package created!')

    def _add_table_file(self, table_name, table_obj, rewrite=True):
        src_file_path = self.get_table_path() + '/' + table_name + '.py'
        src_param = { 'table_obj': table_obj }
        src_content = self.get_rendered_src(tmpl_dir_table+'/table.tmpy', **src_param)
        self.add_file(src_file_path, src_content, rewrite=rewrite)

    def _add_dao_base_file(self):
        src_file_path = self.get_dao_path() + '/_dao.py'
        src_param = {}
        src_content = self.get_rendered_src(tmpl_dir_dao+'/base_dao.tmpy', **src_param)
        self.add_file(src_file_path, src_content)

    def _add_dao_file(self, table_name, dao_obj):
        src_file_path = self.get_dao_path() + '/' + table_name + '_dao.py'
        src_param = { 'dao_obj': dao_obj }
        src_content = self.get_rendered_src(tmpl_dir_dao+'/dao.tmpy', **src_param)
        self.add_file(src_file_path, src_content)

    def _add_service_file(self, service_name, service_obj):
        src_file_path = self.get_service_path() + '/' + service_name + '_service.py'
        src_param = { 'service_obj': service_obj }
        src_content = self.get_rendered_src(tmpl_dir_service+'/service.tmpy', **src_param)
        self.add_file(src_file_path, src_content)


