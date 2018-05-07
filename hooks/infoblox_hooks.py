#!/usr/bin/python

import sys
import json

from charmhelpers.contrib.python import pip_execute

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    config,
    service_name,
    relation_set,
    relation_ids,
    log
)

from infoblox_contexts import InfobloxSubordinateContext

hooks = Hooks()


@hooks.hook('install')
def install():
    pass


@hooks.hook('config-changed',
            'upgrade-charm')
def config_changed():
    pass


@hooks.hook('infoblox-service-relation-joined',
            'infoblox-service-relation-changed')
def relation(rel_id=None):
    pass


if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))
