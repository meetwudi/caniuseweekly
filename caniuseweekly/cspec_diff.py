import enum

import attr

from caniuseweekly.browser import Browser
from caniuseweekly.cspec_types import CSpecVersionStat


def calculate_stat_add(latest_spec, previous_spec):
    results = []
    for browser_code_friendly_name, latest_spec_stats in latest_spec.stats.items():  # noqa: E501
        previous_spec_stats = previous_spec.stats[browser_code_friendly_name]
        new_versions = set(latest_spec_stats.keys()) - \
            set(previous_spec_stats.keys())
        if not new_versions:
            continue
        # usually there will only be one new version
        new_stats = {
            version: latest_spec_stats[version]
            for version in new_versions
        }
        browser = Browser.from_code_friendly_name(browser_code_friendly_name)
        for new_stat in new_stats.items():
            results.append(_CSpecDiffItem(
                browser=browser,
                diff_type=CSpecDiffType.STAT_ADD,
                new_stat=CSpecVersionStat(
                    version=new_stat[0], support=new_stat[1]),
            ))
    return results


@enum.unique
class CSpecDiffType(enum.Enum):
    STAT_ADD = 1


@attr.s
class _CSpecDiffItem():
    browser = attr.ib(validator=attr.validators.instance_of(Browser))
    diff_type = attr.ib(validator=attr.validators.instance_of(CSpecDiffType))
    new_stat = attr.ib()


@attr.s
class CSpecDiff():
    """Difference between two Spec instances.
    """
    stat_add = attr.ib(validator=attr.validators.instance_of(list))
    latest_cspec = attr.ib()

    @classmethod
    def create(cls, latest_cspec, previous_cspec):
        return cls(
            stat_add=calculate_stat_add(latest_cspec, previous_cspec),
            latest_cspec=latest_cspec,
        )

    @property
    def title(self):
        return self.latest_cspec.title

    @property
    def description(self):
        return self.latest_cspec.description

    @property
    def spec(self):
        return self.latest_cspec.spec
