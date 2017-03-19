from unittest import mock

from caniuseweekly.appconfig import appconfig


def test_appconfig_return_env_value():
    with mock.patch.dict('caniuseweekly.appconfig.os.environ', {'caniuseweekly_test_config': 'cool'}):  # noqa: E501
        @appconfig
        def test_config():
            return 'not cool'
        assert test_config() == 'cool'


def test_appconfig_return_hardcode_value():
    @appconfig
    def test_config():
        return 'cool'

    assert test_config() == 'cool'
