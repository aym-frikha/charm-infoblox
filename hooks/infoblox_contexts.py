from charmhelpers.core.hookenv import (
    config,
    service_name,
    log,
    relation_ids
)
from charmhelpers.contrib.openstack.context import (
    OSContextGenerator,
)


class InfobloxSubordinateContext(OSContextGenerator):
    interfaces = ['infoblox-service']

    def __call__(self):
        log('Generating Infoblox configuration')
        ctxt = []

        for rid in relation_ids(self.interfaces[0]):
            self.related = True
            return {
                "neutron": {
                    "/etc/cinder/cinder.conf": {
                        "sections": {
                            service: ctxt
                        }
                    }
                }
            }
