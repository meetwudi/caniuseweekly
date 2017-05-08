import attr

from caniuseweekly.appconfig import appconfig
from caniuseweekly.cspec_diff import CSpecDiff
from caniuseweekly.cspec_loader import cspec_from_feature_json
from caniuseweekly.cspec_loader import feature_json_files
from caniuseweekly.source_repo import get_file_content_by_sha
from caniuseweekly.source_repo import get_source_repo


class DefaultPreviousSHANotDefinedError(Exception):
    pass


@appconfig
def default_previous_sha():
    # Currently, previous_sha needs to be set
    # from environment variables
    raise DefaultPreviousSHANotDefinedError()


def make_issue(previous_sha=None, current_sha=None):
    """Generate a new issue
    """
    repo = get_source_repo()
    if previous_sha is None:
        previous_sha = default_previous_sha()
    if current_sha is None:
        current_sha = str(repo.heads.master.commit)

    previous_feature_json_names = feature_json_files(
        repo=repo,
        sha=previous_sha,
    )
    cspec_diffs = []
    for feature_json_name in previous_feature_json_names:
        previous_cspec = cspec_from_feature_json(
            get_file_content_by_sha(
                repo=repo,
                sha=previous_sha,
                feature_json_name=feature_json_name,
            ),
        )
        current_cspec = cspec_from_feature_json(
            get_file_content_by_sha(
                repo=repo,
                sha=current_sha,
                feature_json_name=feature_json_name,
            ),
        )
        cspec_diff = CSpecDiff.create(
            latest_cspec=current_cspec,
            previous_cspec=previous_cspec,
        )
        cspec_diffs.append(cspec_diff)

    return Issue(
        previous_sha=previous_sha,
        current_sha=current_sha,
        cspec_diffs=cspec_diffs,
    )


@attr.s
class Issue():
    """An issue is a specific version of newsletter that we send to subscribers.
    """
    previous_sha = attr.ib(validator=attr.validators.instance_of(str))
    current_sha = attr.ib(validator=attr.validators.instance_of(str))
    cspec_diffs = attr.ib(validator=attr.validators.instance_of(list))
