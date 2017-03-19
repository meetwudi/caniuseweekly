import tempfile
from unittest import mock

import pytest

from caniuseweekly.source_repo import create_repo_if_does_not_exist
from caniuseweekly.source_repo import GitCloneError
from caniuseweekly.source_repo import source_repo_github_url
from caniuseweekly.source_repo import source_repo_path


def test_create_repo_if_does_not_exist_should_not_create():
    with tempfile.TemporaryDirectory() as tempdirname:
        with mock.patch('caniuseweekly.source_repo.source_repo_path', return_value=tempdirname):  # noqa: E501
            assert not create_repo_if_does_not_exist()


@pytest.mark.parametrize('popen_ret_val', [
    ('a', None),
    ('', 'error'),
])
@mock.patch('caniuseweekly.source_repo.os')
@mock.patch('caniuseweekly.source_repo.subprocess')
def test_create_repo_if_does_not_exist_should_try_to_create(
    mock_sub_process,
    mock_os,
    popen_ret_val,
):
    mock_os.path.exists.return_value = False
    mock_sub_process.Popen().communicate.return_value = popen_ret_val
    if popen_ret_val[1]:
        with pytest.raises(GitCloneError):
            create_repo_if_does_not_exist()
    else:
        create_repo_if_does_not_exist()
        assert mock_sub_process.Popen.called_with([
            'git',
            'clone',
            source_repo_github_url(),
            source_repo_path(),
        ], stdout=mock.ANY)
        assert mock_sub_process.Popen().communicate.called
