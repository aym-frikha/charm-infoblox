import logging
import unittest
import requests

from zaza.utilities import (
    cli as cli_utils,
    openstack as openstack_utils,
)

net_name = 'private'
private_subnet = "192.168.1.0/24"
vm_name = "test_infoblox"
infoblox_ip = "172.27.32.7"
infoblox_username = "admin"
infoblox_password = "infoblox"


def setup_network():
    cli_utils.setup_logging()
    keystone_session = openstack_utils.get_overcloud_keystone_session()
    # Retrieve necessary clients
    keystone_client = openstack_utils.get_keystone_session_client(
        keystone_session)
    neutron_client = openstack_utils.get_neutron_session_client(
        keystone_session)
    # Retrieve necessary variables
    admin_domain = None
    if openstack_utils.get_keystone_api_version() > 2:
        admin_domain = "admin_domain"

    project_id = openstack_utils.get_project_id(
        keystone_client,
        "admin",
        domain_name=admin_domain,
    )
    # Create simple private network

    project_network = openstack_utils.create_project_network(
        neutron_client,
        project_id,
        shared=False,
        network_type="gre")

    openstack_utils.create_project_subnet(
        neutron_client,
        project_id,
        project_network,
        private_subnet,
        ip_version=4)


class InfobloxFunctionalities(unittest.TestCase):

    def test_vm_creation(self):
        """Tests to launch a cirros image."""
        cli_utils.setup_logging()
        keystone_session = openstack_utils.get_overcloud_keystone_session()
        # Retrieve necessary clients
        nova_client = openstack_utils.get_nova_session_client(keystone_session)
        neutron_client = openstack_utils.get_neutron_session_client(
            keystone_session)

        image = nova_client.glance.find_image("cirros")
        flavor = nova_client.flavors.find(name="m1.small")
        networks = neutron_client.list_networks(name=net_name)
        if len(networks['networks']) == 0:
            raise Exception('Network {} has not been created'.format(net_name))
        nics = [{'net-id': networks['networks'][0]['id']}]
        # Launch instance.
        logging.info('Launching instance {}'.format(vm_name))
        instance = nova_client.servers.create(
            name=vm_name,
            image=image,
            flavor=flavor,
            nics=nics)

        # Test Instance is ready.
        logging.info('Checking instance is active')
        openstack_utils.resource_reaches_status(
            nova_client.servers,
            instance.id,
            expected_status='ACTIVE')

    def test_infoblox_api(self):
        """Tests existing data inside infoblox appliance."""
        session = requests.Session()
        session.auth = (infoblox_username, infoblox_password)
        session.verify = False
        url = 'https://' + infoblox_ip + '/wapi/v1.1/'
        r = session.get(url + 'network')
        self.assertEqual(r.json()[0]['network'], private_subnet)
