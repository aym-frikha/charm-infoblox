#!/usr/bin/python2
import subprocess

import charms_openstack.charm
import charmhelpers.core.hookenv as hookenv
from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
)
from charmhelpers.core.host import (
    service_reload,
)
from charmhelpers.contrib.openstack.utils import (
    CompareOpenStackReleases,
    os_release,
)


class InfobloxCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'infoblox'

    # First release supported
    release = 'queens'

    # List of packages to install for this charm
    packages = ['']

    def install(self):
        log('Starting infoblox installation')
        subprocess.check_call(
            ['wget', 'https://github.com/mskalka/networking-infoblox-deb/raw/'
             '/master/networking-infoblox_12.0.0_amd64.deb'])
        subprocess.check_call(
            ['dpkg', '-i', 'networking-infoblox_12.0.0_amd64.deb'])
        service_reload('infoblox-ipam-agent')
        status_set('waiting', 'Incomplete relation: neutron-api

    def create_ea_definitions(self):
        log('Setting up Infoblox EA definitions')
        username = config('admin-user-name')
        password = config('admin-password')
        views = config('network-views')
        subprocess.check_call(
            ['create_ea_defs', '-u', username, '-p', password, '-pnv', views])

    def get_infoblox_conf(self):
        log('Setting neutron-api configuration')
        cfg = {'dc_id': config('cloud-data-center-id'),
               'grid_master_host': config('grid-master-host'),
               'grid_master_name': config('grid-master-name'),
               'admin_user_name': config('admin-user-name'),
               'admin_password': config('admin-password'),
               'wapi_version': config('wapi-version'),
               'wapi_max_results': config('wapi-max-results'),
               'wapi_paging': config('wapi-paging'),
               'network_views': config('network-views'),
               }
        return cfg
