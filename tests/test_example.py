# -*- coding: utf-8 -*-

import json
import logging
import unittest

import fc
from common import RequestType


class TestExample(unittest.TestCase):

    @staticmethod
    def _test_impl(cls_name: str, request_type: RequestType, properties: dict,
                   resource_id: str = None, old_properties: dict = None):
        logging.basicConfig(level=logging.INFO)

        request = {
            'RequestType': request_type.value,
            'ResponseURL': 'https://httpbin.org/post',
            'IntranetResponseURL': 'https://httpbin.org/post',
            'StackId': '8acc3dcd-cf48-4fa1-863e-7c767b61fe42',
            'StackName': 'my-stack',
            'ResourceOwnerId': '123456789',
            'CallerId': '987654321',
            'RegionId': 'cn-hangzhou',
            'RequestId': 'B288A0BE-D927-4888-B0F7-B35EF84B6E6F',
            'ResourceType': f'Custom::{cls_name}',
            'LogicalResourceId': 'my-resource',
            'ResourceProperties': properties,
        }
        if request_type != RequestType.CREATE:
            request['PhysicalResourceId'] = resource_id
        if request_type == RequestType.UPDATE:
            request['OldResourceProperties'] = old_properties

        event = json.dumps(request).encode('utf-8')
        fc.handler(event, None)

    def test_create_example1(self):
        self._test_impl('Example1', RequestType.CREATE, {
            'Year': 2023,
            'City': 'Hangzhou',
        })

    def test_update_example1(self):
        self._test_impl('Example1', RequestType.UPDATE, {
            'Year': 2024,
            'City': 'Hangzhou',
        }, 'example-1698388469.47068', {
            'Year': 2023,
            'City': 'Hangzhou',
        })

    def test_delete_example1(self):
        self._test_impl('Example1', RequestType.DELETE, {
            'Year': 2024,
            'City': 'Hangzhou',
        }, 'example-1698388469.47068')

    def test_create_example2(self):
        self._test_impl('Example2', RequestType.CREATE, {
            'ServerURL': 'https://httpbin.org/post',
            'SshKey': 'xxx'
        })

    def test_delete_example2(self):
        self._test_impl('Example2', RequestType.DELETE, {
            'ServerURL': 'https://httpbin.org/post',
            'SshKey': 'xxx'
        }, '-')

    def test_create_invalid(self):
        self._test_impl('Invalid', RequestType.CREATE, {})
