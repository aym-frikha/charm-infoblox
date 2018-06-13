# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json

from pip import main as pip_execute

import charms_openstack.charm as charm
import charms.reactive as reactive

import charm.openstack.infoblox as infoblox  # noqa

from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
)


charm.use_defaults('update-status')


@reactive.when_not('infoblox.installed')
def install_libraries():
    with charm.provide_charm_instance() as charm_class:
        charm_class.install()
        reactive.set_state('infoblox.installed')
        status_set('active', 'Unit is ready')


@reactive.when('infoblox-neutron.connected')
def configure_neutron_plugin(api_principle):
    with charm.provide_charm_instance() as charm_class:
        log('Setting neutron-api configuration')
        dc_id = config('cloud-data-center-id')
        cfg = {'grid_master_host': config('grid-master-host'),
               'grid_master_name': config('grid-master-name'),
               'admin_user_name': config('admin-user-name'),
               'admin_password': config('admin-password'),
               'wapi_version': config('wapi-version'),
               'wapi_max_results': config('wapi-max-results'),
               'wapi_paging': config('wapi-paging'),
               }
        api_principle.configure_plugin(dc_id=dc_id, config=cfg)


@reactive.when('infoblox-designate.connected')
def configure_designate_plugin(api_principle):
    with charm.provide_charm_instance() as charm_class:
        log('Setting designate configuration')
        dc_id = config('cloud-data-center-id')
        cfg = {}
        api_principle.configure_plgin(dc_id=dc_id, config=cfg)
