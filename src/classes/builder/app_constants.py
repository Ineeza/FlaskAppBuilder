# -*- coding:utf-8 -*-

# this file defines the basic structure to build app.
# basically, should not be modified.

const_src_dir = 'src'
const_builder_dir = 'builder'
const_src_tmpl_dir = 'src_templates'

const_classes_dir = 'classes'
const_controller_dir = 'controller'
const_model_dir = 'model'
const_table_dir = 'table'
const_dao_dir = 'dao'
const_service_dir = 'service'

const_src_file_json = [
    { 'dir': const_classes_dir, 'subtree': [
        { 'dir': const_controller_dir, 'subtree': [] },
        { 'dir': const_model_dir, 'subtree': [
            { 'dir': const_table_dir, 'subtree': [] },
            { 'dir': const_dao_dir, 'subtree': [] },
            { 'dir': const_service_dir, 'subtree': [] },
        ] },
    ] },
]
