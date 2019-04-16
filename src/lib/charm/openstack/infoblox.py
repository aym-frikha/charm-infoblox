#!/usr/bin/python3
import subprocess
import uuid

import charms_openstack.charm
import charmhelpers.core.hookenv as hookenv
from charmhelpers.core.hookenv import (
    config,
    log,
    is_leader,
    leader_set,
    leader_get,
)
from charmhelpers.fetch import (
    apt_install,
    apt_update,
    filter_installed_packages,
    add_source,
)


class InfobloxCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'infoblox'

    # First release supported
    release = 'queens'

    # List of packages to install for this charm
    packages = ['python-networking-infoblox']

    default_service = 'infoblox-ipam-agent'


    def install(self):
        log('Starting infoblox installation')
        installed = len(filter_installed_packages(self.packages)) == 0
        if not installed:
            add_source(config('source'))
            apt_update(fatal=True)
            apt_install(self.packages[0], fatal=True)
        if not leader_get('pool'):
            if is_leader():
                leader_set({'pool': str(uuid.uuid4()),
                            'pool_target': str(uuid.uuid4()),
                            'nameserver': str(uuid.uuid4())})

    def create_ea_definitions(self):
        log('Setting up Infoblox EA definitions')
        username = config('admin-user-name')
        password = config('admin-password')
        views = config('network-views')
        subprocess.check_call(['systemctl', 'restart','infoblox-ipam-agent'])
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
