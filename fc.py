# -*- coding: utf-8 -*-

import json
import logging

import factory


LOG = logging.getLogger(__name__)


def handler(event, context):
    try:
        event = json.loads(event)
        factory.init()
        custom_resource = factory.create(event)
        custom_resource.apply()
    except Exception as ex:
        LOG.exception('unexpected error occurs: %s', ex)
        raise
