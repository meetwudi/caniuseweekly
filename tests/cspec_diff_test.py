from caniuseweekly.browser import BrowserName
from caniuseweekly.cspec_diff import calculate_stat_add
from caniuseweekly.cspec_diff import CSpecDiffType
from testing.cspec import fake_cspec_from_fixture


def test_calculate_stat_add():
    cspec_simple = fake_cspec_from_fixture(id='simple')
    cspec_simple_with_new_stat = fake_cspec_from_fixture(
        id='simple-with-new-stat')
    diffs = calculate_stat_add(
        cspec_simple_with_new_stat,
        cspec_simple,
    )
    assert len(diffs) == 1

    diff = diffs[0]
    assert diff.browser.name == BrowserName.EDGE
    assert diff.new_stat.version == '14'
    assert diff.new_stat.support == 'a'
    assert diff.diff_type == CSpecDiffType.STAT_ADD


def test_calculate_stat_add_multiple_new_stats():
    cspec_simple = fake_cspec_from_fixture(id='simple')
    cspec_simple_with_two_new_stats = fake_cspec_from_fixture(
        id='simple-with-two-new-stats'
    )
    diffs = calculate_stat_add(
        cspec_simple_with_two_new_stats,
        cspec_simple,
    )
    assert len(diffs) == 2
