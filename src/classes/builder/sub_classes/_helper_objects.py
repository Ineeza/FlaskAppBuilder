# -*- coding:utf-8 -*-

''' column type dict for table source-file creations. '''
column_type_string_dict = {
    'BIGINT' : 'BigInteger', 

    'INTEGER' : 'Integer', 
    'MEDIUMINT' : 'Integer', 
    'SMALLINT' : 'Integer', 
    'TINYINT' : 'Integer', 

    'FLOAT' : 'Float', 
    'DOUBLE' : 'Float', 

    'VARCHAR' : 'String', 
    'CHAR' : 'String', 
    'TEXT' : 'String', 
    'LONGTEXT' : 'String', 
    'MEDIUMTEXT' : 'String', 
    'TINYTEXT' : 'String', 

    'BLOB' : 'BLOB', 
    'LONGBLOB' : 'BLOB', 
    'MEDIUMBLOB' : 'BLOB', 
    'TINYBLOB' : 'BLOB', 

    'BINARY' : 'LargeBinary', 
    'VARBINARY' : 'LargeBinary', 

    'DATETIME' : 'DateTime', 
    'TIMESTAMP' : 'DateTime', 

    'DATE' : 'Date', 

    'TIME' : 'Time', 
}

# Now, not support for...
# DECIMAL, YEAR, BIT, ENUM, SET
# CURVE, GEOMETRY, GEOMETRYCOLLECTION, LINESTRING, MULTICURVE, MULTILINESTRING, MULTIPOINT, MULTIPOLYGON, MULTISURFACE
# POINT, POLYGON, SURFACE

column_type_default_dict = {
    'BigInteger' : '0', 
    'Integer' : '0', 
    'Float' : '0', 
    'String' : '', 
    'BLOB' : '', 
    'LargeBinary' : '', 
    'DateTime' : 'None', 
    'Date' : 'None', 
    'Time' : 'None', 
}

''' class for __init__ source-file creations. '''
class ImportObj(object):
    from_name = None
    import_names = []

    def __init__(self, from_name, import_names=[]):
        self.from_name = from_name
        self.import_names = import_names

''' class for table source-file creations. '''
class TableObj(object):
    table_name = None
    table_class_name = None
    columns = None

    def __init__(self, table_name, table_class_name, columns=None):
        self.table_name = table_name
        self.table_class_name = table_class_name
        self.columns = columns

class ColumnObj(object):
    column_name = None
    column_type = None
    primary_key = None
    nullable = None
    autoincrement = None
    default = None

    def __init__(self, column_name, column_type, primary_key, nullable, autoincrement, default=None):
        self.column_name = column_name
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.autoincrement = autoincrement
        self.default = default

''' class for dao source-file creations. '''
class DaoObj(object):
    table_name = None
    table_class_name = None
    dao_class_name = None
    columns = None
    primary_keys = None

    def __init__(self, table_name, table_class_name, dao_class_name, columns=None, primary_keys=None):
        self.table_name = table_name
        self.table_class_name = table_class_name
        self.dao_class_name = dao_class_name
        self.columns = columns
        self.primary_keys = primary_keys

''' class for service source-file creations. '''
class ServiceObj(object):
    service_class_name = None

    def __init__(self, service_class_name):
        self.service_class_name = service_class_name

''' class for controller source-file creations. '''
class ControllerObj(object):
    controller_name = None
    blueprint = None
    url_prefix = None

    def __init__(self, controller_name, blueprint, url_prefix=None):
        self.controller_name = controller_name
        self.blueprint = blueprint
        self.url_prefix = url_prefix


