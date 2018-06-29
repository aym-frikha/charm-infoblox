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


@reactive.when('neutron.configured')
@reactive.when_not('infoblox.installed')
def install_infoblox(principle):
    with provide_charm_instance() as charm_class:
        charm_class.install()
        principle.migrate_principal()
    reactive.set_state('infoblox.installed')


@reactive.when('infoblox.create-defs',
               'infoblox.installed')
def create_ea_definitions():
    with provide_charm_instance() as charm_class:
        charm_class.create_ea_definitions()


@reactive.when('neutron.connected')
def configure_neutron(principle):
    configure_infoblox_principal(principle)


@reactive.when('designate.connected')
def configure_designate(principle):
    configure_infoblox_principal(principle)


def configure_infoblox_principal(principle):
    with provide_charm_instance() as charm_class:
        dc_id, cfg = charm_class.get_infoblox_conf()
        principle.configure_principal(dc_id=dc_id, config=cfg)
