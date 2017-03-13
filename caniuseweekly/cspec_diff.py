import enum

import attr

from caniuseweekly.browser import Browser


def calculate_stat_add(latest_spec, previous_spec):
    results = []
    for browser_code_friendly_name, latest_spec_stats in latest_spec.stats.items():  # noqa: E501
        if browser_code_friendly_name not in previous_spec:
            return

        previous_spec_stats = previous_spec.stats
        new_versions = set(latest_spec_stats.keys()) - \
            set(previous_spec_stats.keys())
        new_stats = {
            version: latest_spec_stats[version]
            for version in new_versions
        }
        browser = Browser.from_code_friendly_name(browser_code_friendly_name)
        results.append(_CSpecDiffItem(
            browser=browser,
            diff_type=CSpecDiffType.STAT_ADD,
            new_stats=new_stats,
        ))


@enum.unique
class CSpecDiffType(enum.Enum):
    STAT_ADD = 1


@attr.s
class _CSpecDiffItem():
    browser = attr.ib(validator=attr.validators.instance_of(Browser))
    diff_type = attr.ib(validator=attr.validators.instance_of(CSpecDiffType))
    new_stats = attr.ib()


@attr.s
class CSpecDiff():
    """Difference between two Spec instances.
    """
    stat_add = attr.ib(validator=attr.validators.instance_of(list))
    spec_change = attr.ib(validator=attr.validators.instance_of(list))

    @classmethod
    def create(cls, latest_cspec, previous_cspec):
        return cls(
            stat_add=calculate_stat_add(latest_cspec, previous_cspec),
        )
