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
    set_flag,
    clear_flag
)
from charmhelpers.core.hookenv import status_set
from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
)
import charm.openstack.infoblox as infoblox  # noqa


use_defaults('update-status')


@when_not('infoblox.installed')
@when('neutron.available')
def install_infoblox():
    with provide_charm_instance() as charm_class:
        charm_class.install()
    set_flag('infoblox.installed')


@when_all('infoblox.installed',
          'neutron.available',
          'neutron.configured')
@when_not('create-ea-definitions.done')
def create_ea_definitions():
    principal_neutron = \
        endpoint_from_flag('neutron.available')
    if principal_neutron.principal_charm_state() == "True":
        with provide_charm_instance() as charm_class:
            charm_class.create_ea_definitions()
        status_set('active', 'Unit is ready')
        set_flag('create-ea-definitions.done')


@when_all('infoblox.installed',
          'neutron.available')
@when_not('neutron.configured')
def configure_neutron(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_neutron_conf()
        principal_neutron = \
            endpoint_from_flag('neutron.available')
        principal_neutron.configure_principal(config)
        clear_flag('create-ea-definitions.done')
        set_flag('neutron.configured')


@when('designate.connected')
@when('infoblox.installed')
@when_not('designate.configured')
def configure_designate(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_designate_conf()
        if config:
            principle.configure_principal(config)
            set_flag('designate.configured')
