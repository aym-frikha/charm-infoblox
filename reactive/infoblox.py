#!/usr/bin/python

import sys
import json

from pip import main as pip_execute

from charms.reactive import (
    hook,
    set_state,
    remove_state,
    when,
    when_not,
)

from charms.layer.infobloxutils import (
    NeutronSubordinateContext,
    DesignateSubordinateContext,
    get_infoblox_version,
)

from charmhelpers.fetch import (
    apt_purge,
)

from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
    relation_ids,
    relation_set,
)


@when_not('infoblox.installed')
def install():
    pip_execute(
        ['install', 'networking-infoblox{}'.format(get_infoblox_version()),
         '--no-deps'])
    status_set('active', 'Unit is ready')
    set_state('infoblox.installed')


@when('config.changed',
      'infoblox.installed')
def config_changed():
    status_set('maintenance', 'Configuration changed, updating related units.')
    for rid in relation_ids('neutron-infoblox'):
        neutron_relation(rel_id=rid)
    for rid in relation_ids('desigate-infoblox'):
        desigate_relation(rel_id=rid)
    status_set('active', 'Unit is ready')


@when('neutron-plugin-api-subordinate.connected',
      'infoblox.installed')
def neutron_relation(api_principle):
    api_principle.configure_plugin(
        subordinate_configuration=NeutronSubordinateContext()())
    api_principle.request_restart()


@when('desigate.connected',
      'infoblox.installed')
def designate_relation(rel_id=None):
    relation_set(
        relation_id=rel_id,
        subordinate_configuration=json.dumps(
            DesignateSubordinateContext()())
    )
