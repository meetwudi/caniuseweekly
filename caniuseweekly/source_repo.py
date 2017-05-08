import logging
import os
import subprocess

import git

from caniuseweekly.appconfig import appconfig

logger = logging.getLogger(__name__)


class GitCloneError(Exception):
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
