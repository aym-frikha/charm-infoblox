#!/usr/bin/env python3

# Copyright 2019 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Encapsulate infoblox testing."""

import logging
import uuid

import zaza.model
import zaza.charm_tests.test_utils as test_utils
import zaza.utilities.openstack as openstack_utils
import zaza.charm_tests.nova.utils as nova_utils


class InfobloxTest(test_utils.OpenStackBaseTest):
    """Encapsulate Infoblox tests."""

    @classmethod
    def setUpClass(cls):
        """Run class setup for running tests."""
        super(InfobloxTest, cls).setUpClass()
        cls.keystone_session = openstack_utils.get_overcloud_keystone_session()
        cls.model_name = zaza.model.get_juju_model()
        cls.neutron_client = openstack_utils.get_cinder_session_client(
            cls.keystone_session)
        cls.nova_client = openstack_utils.get_nova_session_client(
            cls.keystone_session)
