#!/usr/local/sbin/charm-env python3
# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

import charmhelpers.core.hookenv as hookenv
import charms.reactive


def force_service_restart(*args):
    cmds = [
        ['neutron-db-manage', 'upgrade', 'head'],
        ['service', 'infoblox-ipam-agent', 'restart'],
        ['service', 'neutron-server', 'restart'],
    ]
    for cmd in cmds:
        subprocess.check_call(cmd)


def main(args):
    action_name = os.path.basename(args[0])
    try:
        action = ACTIONS[action_name]
    except KeyError:
        return "Action %s undefined" % action_name
    else:
        try:
            action(args)
        except Exception as e:
            hookenv.action_fail(str(e))
        else:
            charms.reactive.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
