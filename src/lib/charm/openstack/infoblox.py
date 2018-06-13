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
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'ocata':
        return '==10.0.1'
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'pike':
        return '==11.0.1'
    else:
        return None


class InfobloxCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'infoblox'

    # First release supported
    release = 'mitaka'

    # List of packages to install for this charm
    packages = ['']
    # FIXME: This ugly hack. Package networking-infoblox?
    def install(self):
        deps = ['chardet', 'idna', 'pytz', 'pyparsing', 'pbr', 'funcsigs',
                'six', 'wrapt', 'debtcollector', 'iso8601', 'Babel',
                'oslo.i18n', 'netifaces', 'netaddr', 'monotonic', 'oslo.utils',
                'msgpack', 'oslo.serialization', 'python-dateutil',
                'pyinotify', 'oslo.context', 'enum34', 'PyYAML', 'stevedore',
                'rfc3986', 'oslo.config', 'oslo.log', 'setuptools',
                'infoblox-client']
        pip_execute(
            ['install', '--install-option="--install-data=/"',
             'networking-infoblox{}'.format(get_infoblox_version()),
             '--no-deps'])
        for dep in deps:
            pip_execute(['install', dep, '--no-deps'])
