import logging
import os
import subprocess
from contextlib import contextmanager

import git

from caniuseweekly.appconfig import appconfig

logger = logging.getLogger(__name__)


class GitCloneError(Exception):
    pass


class RepoIsDirtyError(Exception):
    pass


@appconfig
def source_repo_github_url():
    return 'git@github.com:Fyrd/caniuse.git'


@appconfig
def source_repo_path():
    return os.path.expanduser('~/caniuseweekly')


def create_repo_if_does_not_exist():
    """
    :returns: True when no repo cloned, otherwise False
    """
    if os.path.exists(source_repo_path()):
        return False
    logger.info('Source repository not found at {}, trying to create one'.format(source_repo_path()))  # noqa: E501
    clone_output, clone_err = subprocess.Popen([
        'git',
        'clone',
        source_repo_github_url(),
        source_repo_path(),
    ], stdout=subprocess.PIPE).communicate()

    if clone_err:
        logger.error(clone_err)
        raise GitCloneError
    logger.info(clone_output)
    return True


def get_source_repo():
    create_repo_if_does_not_exist()
    return git.Repo(source_repo_path())


def get_file_content_by_sha(repo, sha, filepath):
    return repo.git.show('{}:{}'.format(sha, filepath))


@contextmanager
def checkout_and_exit_clean(repo, sha):
    """Checkout to a commit with specific SHA and checkout back the previous
    branch.
    """
    # current working directory must be clean
    if repo.is_dirty():
        raise RepoIsDirtyError()

    # save current ref's SHA
    saved_head_commit_sha = str(repo.head.object)

    repo.git.checkout(sha)
    yield

    # repo should be clean at this point as well
    if repo.is_dirty():
        raise RepoIsDirtyError()

    # switch back to previous commit
    repo.git.checkout(saved_head_commit_sha)
