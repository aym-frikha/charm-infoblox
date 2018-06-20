import mock

import reactive.infoblox_handlers as handlers

import charms_openstack.test_utils as test_utils


CHARM_CONFIG = {'grid-master-host': 'https://1.1.1.1',
                'grid-master-name': 'infoblox.localhost',
                'admin-user-name': 'openstack',
                'admin-password': 'openstack',
                'wapi-version': '2'}


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        # test that the hooks actually registered the relation expressions that
        # are meaningful for this interface: this is to handle regressions.
        # The keys are the function names that the hook attaches to.
        hook_set = {
            'when': {
                'configure_neutron_plugin': ('infoblox-neutron.connected', ),
            },
            'when_not': {
                'install_packages': ('infoblox.installed', ),
            },
        }
        # test that the hooks were registered via the
        # reactive.infoblox_handlers
        self.registered_hooks_test_helper(handlers, hook_set, [])


class TestHandlers(test_utils.PatchHelper):

    def __init__(self):
        self.patch('charmhelpers.core.hookenv.config', )

    def _patch_provide_charm_instance(self):
        the_charm = mock.MagicMock()
        self.patch_object(handlers, 'provide_charm_instance',
                          name='provide_charm_instance',
                          new=mock.MagicMock())
        self.provide_charm_instance().__enter__.return_value = the_charm
        self.provide_charm_instance().__exit__.return_value = None
        return the_charm

    def test_install_packages(self):
        the_charm = self._patch_provide_charm_instance()
        self.patch_object(handlers.reactive, 'set_state')
        self.patch_object(handlers.reactive, 'remove_state')
        handlers.install_packages()
        the_charm.install.assert_called_once_with()
        calls = [mock.call('infoblox.installed')]
        self.set_state.assert_has_calls(calls)

    def test_configure_neutron_plugin(self):
        neutron = mock.MagicMock()
        handlers.configure_neutron_plugin(neutron)
        neutron.configure_plugin.assert_called_once_with(
            dc_id='0', cfg={})
