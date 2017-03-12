from unittest import mock

import pytest

from caniuseweekly.validators import dict_validator
from caniuseweekly.validators import DictValidatorKeypathDoesNotExistError


PARAM_NOT_USED = None


class TestDictValidation():

    @pytest.mark.parametrize('required_keypaths, attr_value', [
        [['key'], {}],
        [['key.a'], {}],
        [['key.a'], {'key': {}}],
    ])
    def test_should_raise_when_keypath_does_not_exist(
        self,
        required_keypaths,
        attr_value
    ):
        v = dict_validator(required_keypaths)
        with pytest.raises(DictValidatorKeypathDoesNotExistError) as exec_info:
            v(PARAM_NOT_USED, PARAM_NOT_USED, attr_value)
            assert "'key' not found" in str(exec_info.value)

    @pytest.mark.parametrize('required_keypaths, attr_value', [
        [['key'], {'key': 1}],
        [[], {'key': 1}],  # empty required_keypaths should still pass
        [['key.a'], {'key': {'a': 1}}],
        [['key', 'key2'], {'key': 1, 'key2': 3}],
    ])
    def test_should_not_raise_when_keypath_do_exist(
        self,
        required_keypaths,
        attr_value
    ):
        v = dict_validator(required_keypaths)
        v(PARAM_NOT_USED, PARAM_NOT_USED, attr_value)

    def test_should_raise_when_is_not_a_dict(self):
        v = dict_validator([])
        mock_attr = mock.Mock()
        mock_name = mock.PropertyMock(return_value='myattr')
        type(mock_attr).name = mock_name
        with pytest.raises(TypeError) as exec_info:
            v(PARAM_NOT_USED, mock_attr, 1)
            assert "'myattr' must be a dict object." in str(exec_info.value)
