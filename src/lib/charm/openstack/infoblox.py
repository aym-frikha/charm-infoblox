import subprocess

from pip import main as pip_execute

import charmhelpers.core.hookenv as hookenv
from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
)
import charms_openstack.charm

from charmhelpers.contrib.openstack.utils import (
    CompareOpenStackReleases,
    os_release,
)


def get_infoblox_version():
    """if CompareOpenStackReleases(os_release('neutron-server')) == 'mitaka':
        return '==8.0.1'
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'newton':
        return '==9.0.1'
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'ocata':
        return '==10.0.1'
    elif CompareOpenStackReleases(os_release('neutron-server')) == 'pike':
        return '==11.0.1'
    else:"""
    return '==12.0.0'


class InfobloxCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'infoblox'

    # First release supported
    release = 'mitaka'

    # List of packages to install for this charm
    packages = ['']
    # FIXME: This is an ugly hack. Package networking-infoblox?

    def install(self):
        log('Starting infoblox installation')
        subprocess.check_call(
            ['pip', 'install',
             'networking-infoblox{}'.format(get_infoblox_version()),
             "--install-option=--install-data=/"])
        hookenv.log('Starting infoblox-ipam-agent service')
        subprocess.check_call(
            ['update-rc.d', 'infoblox-ipam-agent', 'defaults'])
        subprocess.check_call(
            ['service', 'infoblox-ipam-agent', 'restart'])
        status_set('active', 'Unit is ready')


    def create_ea_definitions(self):
        log('Setting up Infoblox EA definitions')
        username = config('admin-user-name')
        password = config('admin-password')
        views = config('network-views')
        subprocess.check_call(
            ['create_ea_defs', '--username', username, '--password', password,
             '--participating_network_views', views])

    def get_infoblox_conf(self):
        log('Setting neutron-api configuration')
        cfg = {'grid_master_host': config('grid-master-host'),
               'grid_master_name': config('grid-master-name'),
               'admin_user_name': config('admin-user-name'),
               'admin_password': config('admin-password'),
               'wapi_version': config('wapi-version'),
               'wapi_max_results': config('wapi-max-results'),
               'wapi_paging': config('wapi-paging'),
               }
        dc_id = config('cloud-data-center-id')
        return dc_id, cfg
