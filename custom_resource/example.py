# -*- coding: utf-8 -*-

import time
import random
import logging
import requests
from typing import Optional

from common import BaseCustomResource


LOG = logging.getLogger(__name__)


class Example1(BaseCustomResource):

    def handle_create(self) -> Optional[str]:
        LOG.info('[create] request id: %s', self.request_id)
        LOG.info('[create] properties: %s', self.resource_properties)
        return f'example-{time.time()}'

    def handle_update(self, prop_diff):
        LOG.info('[update] request id: %s', self.request_id)
        LOG.info('[update] resource id: %s', self.physical_resource_id)
        LOG.info('[update] properties: %s', self.resource_properties)
        LOG.info('[update] old properties: %s', self.old_resource_properties)
        LOG.info('[update] prop diff: %s', prop_diff)

    def handle_delete(self):
        LOG.info('[delete] request id: %s', self.request_id)
        LOG.info('[delete] resource id: %s', self.physical_resource_id)
        LOG.info('[delete] properties: %s', self.resource_properties)

    def get_outputs(self) -> Optional[dict]:
        return dict(
            RandomNumber=random.randint(0, 10000),
            Id=self.physical_resource_id,
        )


class Example2(BaseCustomResource):

    def _request(self, data):
        server_url = self.resource_properties['ServerURL']
        resp = requests.post(server_url, json=data)
        LOG.info('[request] response: %s %s', resp.status_code, resp.content.decode('utf-8'))

    def handle_create(self) -> Optional[str]:
        self._request(dict(
            Action='AddSshKey',
            SshKey=self.resource_properties['SshKey'],
        ))
        return None

    def handle_delete(self):
        self._request(dict(
            Action='RemoveSshKey',
            SshKey=self.resource_properties['SshKey'],
        ))
