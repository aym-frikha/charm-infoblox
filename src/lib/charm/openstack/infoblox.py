#!/usr/bin/python2
import subprocess
import uuid

import charms_openstack.charm
import charmhelpers.core.hookenv as hookenv
from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
    is_leader,
    leader_set,
    leader_get,
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

    def install(self, neutron=False):
        log('Starting infoblox installation')
        if neutron:
            subprocess.check_call(
                ['wget', 'https://github.com/mskalka/networking-infoblox-'
                'deb/raw/master/networking-infoblox_12.0.0_amd64.deb'])
            subprocess.check_call(
                ['dpkg', '-i', 'networking-infoblox_12.0.0_amd64.deb'])
            subprocess.check_call(
                ['service', 'infoblox-ipam-agent', 'restart'])

        if not leader_get('pool'):
            if is_leader():
                leader_set({'pool': str(uuid.uuid4()),
                            'pool_target': str(uuid.uuid4()),
                            'nameserver': str(uuid.uuid4())})
        status_set('active', 'Unit is ready')

    def create_ea_definitions(self):
        log('Setting up Infoblox EA definitions')
        username = config('admin-user-name')
        password = config('admin-password')
        views = config('network-views')
        subprocess.check_call(['service', 'infoblox-ipam-agent', 'restart'])
        subprocess.check_call(
            ['create_ea_defs', '-u', username, '-p', password, '-pnv', views])

    def get_neutron_conf(self):
        return {'dc_id': config('cloud-data-center-id'),
                'grid_master_host': config('grid-master-host'),
                'grid_master_name': config('grid-master-name'),
                'admin_user_name': config('admin-user-name'),
                'admin_password': config('admin-password'),
                'wapi_version': config('wapi-version'),
                'wapi_max_results': config('wapi-max-results'),
                'wapi_paging': config('wapi-paging'),
                'network_views': config('network-views'),
                }

    def get_designate_conf(self):
        if leader_get('pool'):
            pool_uuid = leader_get('pool')
            pool_target_uuid = leader_get('pool_target')
            nameserver_uuid = leader_get('nameserver')
        else:
            log('Designate UUIDS not yet set by leader, skipping for now.')
            return None
        return {
            'pool': pool_uuid,
            'pool_target': pool_target_uuid,
            'nameserver': nameserver_uuid,
            'host': config('grid-master-host'),
            'wapi_version': config('wapi-version'),
            'admin_username': config('admin-user-name'),
            'admin_password': config('admin-user-password'),
            }
