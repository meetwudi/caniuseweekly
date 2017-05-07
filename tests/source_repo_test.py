import os
import tempfile
from unittest import mock

import git
import pytest

from caniuseweekly.source_repo import create_repo_if_does_not_exist
from caniuseweekly.source_repo import get_file_content_by_sha
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


def test_get_file_content_by_sha():
    content_revisions = [
        'abc',
        'def',
        'geh',
    ]
    commits = []
    filename = 'testfile'
    with tempfile.TemporaryDirectory() as tempdirname:
        repo = git.Repo.init(tempdirname)
        for content_revision in content_revisions:
            with open(os.path.join(tempdirname, filename), 'w') as fp:
                fp.write(content_revision)
            repo.index.add([filename])
            commits.append(repo.index.commit('New Commit'))
        for content_revision, commit in zip(content_revisions, commits):
            assert get_file_content_by_sha(
                repo, str(commit), filename) == content_revision
        # should raise when commit doesn't exist
        with pytest.raises(git.exc.GitCommandError) as exc_info:
            get_file_content_by_sha(repo, 'abcdef', filename)
            assert "Invalid object name 'abcdef'" in str(exc_info)
