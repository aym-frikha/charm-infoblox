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

import charms.reactive as reactive

from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
)
import charm.openstack.infoblox as infoblox  # noqa


use_defaults('update-status')


@reactive.when_not('infoblox.installed')
def install_infoblox():
    with provide_charm_instance() as charm_class:
        charm_class.install()
    reactive.set_state('infoblox.installed')


@reactive.hook('config-changed')
def config_changed():
    reactive.remove_state('neutron.configured')
    reactive.remove_state('designate.configured')


@reactive.when('infoblox.create-defs')
@reactive.when('infoblox.installed')
@reactive.when_not('infoblox.ready')
def create_ea_definitions():
    with provide_charm_instance() as charm_class:
        charm_class.create_ea_definitions()
    reactive.set_state('infoblox.ready')


@reactive.when('neutron.connected')
@reactive.when('infoblox.installed')
@reactive.when_not('neutron.configured')
def configure_neutron(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_neutron_conf()
        principle.configure_principal(config)
    reactive.set_state('neutron.configured')


@reactive.when('designate.connected')
@reactive.when('infoblox.installed')
@reactive.when_not('designate.configured')
def configure_designate(principle):
    with provide_charm_instance() as charm_class:
        config = charm_class.get_designate_conf()
        if config:
            principle.configure_principal(config)
            reactive.set_state('designate.configured')
