# Copyright 2019 Canonical Ltd
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

from charms.reactive import (
    endpoint_from_flag,
    when,
    when_not,
    when_all,
    set_flag
)
from charmhelpers.core.hookenv import status_set
from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
)
import charm.openstack.infoblox as infoblox  # noqa


use_defaults('update-status')


@when_not('infoblox.installed')
@when('endpoint.neutron.connected')
def install_infoblox():
    with provide_charm_instance() as charm_class:
        charm_class.install()
    set_flag('infoblox.installed')


@when_all('endpoint.neutron.neutron_server_ready',
          'infoblox.installed')
@when_not('infoblox.ready')
def create_ea_definitions():
    with provide_charm_instance() as charm_class:
        charm_class.create_ea_definitions()
    status_set('active', 'Unit is ready')
    set_flag('infoblox.ready')


@when_all('infoblox.installed',
          'endpoint.neutron.connected')
@when_not('endpoint.neutron.configured')
def configure_neutron(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_neutron_conf()
        principal_neutron = \
            endpoint_from_flag('endpoint.neutron.connected')
        principal_neutron.configure_principal(config)
    set_flag('endpoint.neutron.configured')


@when('designate.connected')
@when('infoblox.installed')
@when_not('designate.configured')
def configure_designate(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_designate_conf()
        if config:
            principle.configure_principal(config)
            set_flag('designate.configured')
