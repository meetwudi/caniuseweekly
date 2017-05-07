import attr

from caniuseweekly.appconfig import appconfig
from caniuseweekly.cspec_diff import CSpecDiff
from caniuseweekly.cspec_loader import cspec_from_feature_json
from caniuseweekly.source_repo import feature_json_files
from caniuseweekly.source_repo import get_feature_json_by_sha
from caniuseweekly.source_repo import get_latest_sha
from caniuseweekly.source_repo import get_source_repo


class PreviousSHANotDefinedError(Exception):
    pass


@appconfig
def previous_sha():
    # Currently, previous_sha needs to be set
    # from environment variables
    raise PreviousSHANotDefinedError()


def make_issue(previous_sha=previous_sha(), current_sha=None):
    """Generate a new issue
    """
    repo = get_source_repo()
    if current_sha is None:
        current_sha = get_latest_sha(repo)

    previous_feature_json_names = feature_json_files(
        repo=repo,
        sha=previous_sha,
    )
    cspec_diffs = []
    for feature_json_name in previous_feature_json_names:
        previous_cspec = cspec_from_feature_json(
            get_feature_json_by_sha(
                repo=repo,
                sha=previous_sha,
                feature_json_name=feature_json_name,
            ),
        )
        current_cspec = cspec_from_feature_json(
            get_feature_json_by_sha(
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
    current_sha = attr.ib(validators=attr.validators.instance_of(str))
    cspec_diffs = attr.ib(validators=attr.validators.instance_of(list))
