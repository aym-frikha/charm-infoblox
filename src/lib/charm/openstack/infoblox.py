import socket
import subprocess

from pip import main as pip_execute

import charmhelpers.core.hookenv as hookenv
import charmhelpers.contrib.network.ip as ch_ip
import charms_openstack.charm

from charmhelpers.contrib.openstack.utils import (
    CompareOpenStackReleases,
    os_release,
)

def get_infoblox_version():
    if CompareOpenStackReleases(os_release('neutron-server')) <= 'mitaka':
        return '==8.0.1'
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'newton':
        return '==9.0.1'
    else:
        return None

class InfobloxCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'infoblox'

    # First release supported
    release = 'mitaka'

    # List of packages to install for this charm
    packages = ['']

    def install(self):
        pip_execute(
            ['install', 'networking-infoblox{}'.format(get_infoblox_version()),
             '--no-deps'])
