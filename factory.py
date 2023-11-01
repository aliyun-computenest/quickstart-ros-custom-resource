# -*- coding: utf-8 -*-

import os
import pkgutil

import custom_resource
from common import BaseCustomResource
from util import camel_style_to_c_style


class UnsupportedCustomResource(BaseCustomResource):

    def handle_create(self):
        if self.resource_type:
            raise Exception('unsupported custom resource type: {}'.format(self.resource_type))
        else:
            raise Exception('custom resource type not specified, '
                            'using Custom::XXX instead of Aliyun::ROS::CustomResource, '
                            'where XXX is the name of the custom resource class.')

    def handle_delete(self):
        pass


class Factory:

    RESOURCE_TYPE_PREFIX = 'Custom::'

    def __init__(self):
        self._inited = False
        self._resource_type_lookup = {}

    def init(self):
        if self._inited:
            return

        def on_error(name):
            raise

        for _, sub_module_name, is_pkg in pkgutil.walk_packages(
                custom_resource.__path__, f'{custom_resource.__name__}.', on_error):
            if is_pkg:
                continue
            sub_module = __import__(sub_module_name, fromlist=[sub_module_name.rpartition('.')[0]])
            for k in dir(sub_module):
                if k.startswith('_'):
                    continue
                v = getattr(sub_module, k)
                if not isinstance(v, type):
                    continue
                if not issubclass(v, BaseCustomResource) or v == BaseCustomResource:
                    continue
                cls_name = f'{self.RESOURCE_TYPE_PREFIX}{v.__name__}'
                if cls_name in self._resource_type_lookup:
                    raise Exception(f'duplicate custom resource class name: {cls_name}')
                self._resource_type_lookup[cls_name] = v

        self._inited = True

    def create(self, kwargs):
        params = {}
        for k, v in kwargs.items():
            params[camel_style_to_c_style(k)] = v
        resource_type = params.get('resource_type')
        if resource_type == 'ALIYUN::ROS::CustomResource':
            resource_type = os.environ.get('ResourceType')
        if resource_type:
            cls = self._resource_type_lookup.get(resource_type)
        else:
            cls = None
        if not cls:
            cls = UnsupportedCustomResource
        try:
            r = cls(**params)
            r.resource_type = resource_type
            return r
        except Exception as ex:
            msg = f'unable to instantiate custom resource: {ex}'
            raise Exception(msg)


_inst = Factory()
init = _inst.init
create = _inst.create
