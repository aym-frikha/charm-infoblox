# Overview

This subordinate charm provides an Infoblox integration with OpenStack Neutron.

# Usage

With the OpenStack neutron-api charm:

    juju deploy infoblox
    juju deploy neutron-api
    juju add-relation neutron-api infoblox

# Configuration Options


# Restrictions

Compatible with OpenStack Queens and higher, requires a configured Infoblox server.

# Infoblox setup process

Basically this charm setup the infoblox IPAM driver for openstack neutron.
It follows process provided in the Infoblox documentation:
https://docs.infoblox.com/display/ipamdriverosneutron/Installing+Infoblox+IPAM+Driver+for+OpenStack+Neutron

Basically 4 steps are done by this charm:
1- Install the infoblox module on neutron-api nodes.
2- Send configuration to Neutron-api charm to update neutron.conf file and do
the db migration (To create the Infoblox tables)
3- Send extendible attributes to the Infoblox appliance
4- Restart the infoblox-ipam service
