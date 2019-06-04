import mock

import reactive.infoblox_handlers as handlers

import charms_openstack.test_utils as test_utils


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        # test that the hooks actually registered the relation expressions that
        # are meaningful for this interface: this is to handle regressions.
        # The keys are the function names that the hook attaches to.
        hook_set = {
            'when_all': {
                'configure_neutron': ('infoblox.installed',
                                      'neutron.available', ),
                'create_ea_definitions': (
                    'neutron.configured',
                    'neutron.available',
                    'infoblox.installed', )
            },
            'when_not': {
                'install_infoblox': ('infoblox.installed', ),
                'configure_designate': ('designate.configured',),
                'create_ea_definitions': ('create-ea-definitions.done',),
                'configure_neutron': ('neutron.configured',)
            },
        }
        # test that the hooks were registered via the
        # reactive.infoblox_handlers
        self.registered_hooks_test_helper(handlers, hook_set, [])


class TestHandlers(test_utils.PatchHelper):

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
        self.patch_object(handlers, 'set_flag')
        handlers.install_infoblox()
        the_charm.install.assert_called_once_with()
        calls = [mock.call('infoblox.installed')]
        self.set_flag.assert_has_calls(calls)
