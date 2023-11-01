# -*- coding: utf-8 -*-

import abc
import enum
import time
import json
import logging
from typing import Optional, Union
from urllib.request import Request, urlopen


LOG = logging.getLogger(__name__)


class RequestType(enum.Enum):

    CREATE = 'Create'
    UPDATE = 'Update'
    DELETE = 'Delete'


class BaseCustomResource(metaclass=abc.ABCMeta):

    def __init__(self, request_type: Union[RequestType, str], response_url: str,
                 intranet_response_url: str, stack_id: str, stack_name: str, resource_owner_id: str, caller_id: str,
                 region_id: str, request_id: str, resource_type: str, logical_resource_id: str,
                 resource_properties: dict, physical_resource_id: Optional[str] = None,
                 old_resource_properties: Optional[dict] = None):
        self.request_type: RequestType = (request_type if isinstance(request_type, RequestType) else
                                          RequestType(request_type))
        self.response_url = response_url
        self.intranet_response_url = intranet_response_url
        self.stack_id = stack_id
        self.stack_name = stack_name
        self.resource_owner_id = resource_owner_id
        self.caller_id = caller_id
        self.region_id = region_id
        self.request_id = request_id
        self.resource_type = resource_type
        self.logical_resource_id = logical_resource_id
        self.resource_properties = resource_properties
        self.physical_resource_id = physical_resource_id
        self.old_resource_properties = old_resource_properties

    def apply(self):
        resp = dict(
            RequestId=self.request_id,
            LogicalResourceId=self.logical_resource_id,
            StackId=self.stack_id,
        )
        func = getattr(self, self.request_type.value.lower())
        try:
            data = func()
        except Exception as ex:
            resp.update(
                Status='FAILED',
                Reason=str(ex)
            )
        else:
            resp.update(
                Status='SUCCESS',
                PhysicalResourceId=self.physical_resource_id
            )
            if data is not None:
                resp.update(
                    Data=data
                )

        self._notify(resp)

    def _notify(self, resp):
        retry_count = 10
        while retry_count > 0:
            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'Date': time.strftime('%a, %d %b %Y %X GMT', time.gmtime())
            }
            body = json.dumps(resp)
            body = body.encode('utf-8')
            req = Request(self.response_url, data=body, headers=headers)
            resp = urlopen(req, timeout=20)
            resp_content = resp.read()
            resp_content = resp_content.decode('utf-8')
            LOG.info('notify result: %s %s', resp.status, resp_content)
            if resp.status >= 500:
                retry_count -= 1
                continue
            break
        else:
            raise Exception('notify retry expired')

    def create(self) -> Optional[dict]:
        r = self.handle_create()
        if r is None or r == '':
            r = '-'
        elif not isinstance(r, str):
            r = str(r)
        self.physical_resource_id = r
        return self.get_outputs()

    def update(self) -> Optional[dict]:
        if not self.physical_resource_id:
            return
        prop_diff = self._get_props_diff()
        if not prop_diff:
            return
        self.handle_update(prop_diff)
        return self.get_outputs()

    def delete(self) -> None:
        if not self.physical_resource_id:
            return
        self.handle_delete()

    def _get_props_diff(self):
        if self.request_type != RequestType.UPDATE:
            return {}
        old_props = self.old_resource_properties or {}
        new_props = self.resource_properties or {}
        props_diff = {}
        for name, old_value in old_props.items():
            new_value = new_props.get(name)
            if old_value != new_value:
                props_diff[name] = (old_value, new_value)
        for name, new_value in new_props.items():
            if name in old_props:
                continue
            props_diff[name] = (None, new_value)
        return props_diff

    @abc.abstractmethod
    def handle_create(self) -> Optional[str]:
        return None

    def handle_update(self, prop_diff):
        raise Exception('resource update is not supported.')

    @abc.abstractmethod
    def handle_delete(self):
        return

    def get_outputs(self) -> Optional[dict]:
        return None
