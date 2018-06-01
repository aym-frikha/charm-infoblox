from charmhelpers.core.hookenv import (
    config,
    service_name,
    log,
    relation_ids,
    related_units,
)
from charmhelpers.contrib.openstack.context import (
    OSContextGenerator,
)

from charmhelpers.contrib.openstack.utils import (
    os_release,
)

def get_infoblox_version():
    if os_release <= 'mitaka':
        return '=8.0.1'
    elif os_release == 'newton':
        return '=9.0.1'
    else:
        return None


class NeutronSubordinateContext(OSContextGenerator):
    interfaces = ['neutron-infoblox']

    def __call__(self):
        log('Generating Infoblox configuration')
        ctxt = []
        charm_config = config()
        service = 'Infoblox'
        if config('cloud_data_center_id'):
            service = '-dc:'.join([service, config('cloud_data_center_id')])

        for key in charm_config.keys():
            ctxt.append((key.replace('-', '_'), charm_config[key]))

        for rid in relation_ids(self.interfaces[0]):
            self.related = True
            return {
                'neutron-api': {
                    '/etc/neutron/neutron.conf': {
                        'sections': {
                            'DEFAULT': [('ipam_driver', 'infoblox')],
                            'infoblox': [('cloud_data_center_id', '1')],
                            service: ctxt
                        }
                    }
                }
            }


class DesignateSubordinateContext(OSContextGenerator):
    interfaces = ['designate-infoblox']

    def __call__(self):
        log('Generating Infoblox configuration')
        ctxt = self.generate_context()
        log(ctxt)
        service = 'Infoblox'
        if config('cloud_data_center_id'):
            service = '-'.join([service, config('cloud_data_center_id')])

        for rid in relation_ids(self.interfaces[0]):
            self.related = True
            return {
                'designate': {
                    '/etc/designate/designate.conf': {
                        'sections': {
                            service: ctxt
                        }
                    }
                }
            }

    def generate_context(self):
        ctxt = []
        charm_config = config()
        for key in charm_config.keys():
            ctxt.append((key.replace('-', '_'), charm_config[key]))
        return ctxt
