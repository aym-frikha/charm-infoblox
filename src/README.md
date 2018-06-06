# Overview

This subordinate charm provides an Infoblox integration with OpenStack Neutron.

# Usage

With the OpenStack neutron-api charm:

    juju deploy infoblox
    juju deploy neutron-api
    juju add-relation neutron-api infoblox

# Configuration Options


# Restrictions

Compatible with OpenStack Mitaka and higher, requires a configured Infoblox server.
