import pytest

from caniuseweekly.cspec_types import CSpecVersionStat
from caniuseweekly.cspec_types import note_num_from_version_stat


def test_note_num_from_version_stat():
    assert note_num_from_version_stat(CSpecVersionStat(
        version='dont_use_me',
        support='a #12',
    )) == 12
    assert note_num_from_version_stat(CSpecVersionStat(
        version='dont_use_me',
        support='a # 12 ',
    )) == 12
    assert note_num_from_version_stat(CSpecVersionStat(
        version='dont_use_me',
        support='a',
    )) is None

    with pytest.raises(Exception):
        note_num_from_version_stat(CSpecVersionStat(
            version='dont_use_me',
            support='a#not_a_int',
        ))
    with pytest.raises(Exception):
        note_num_from_version_stat(CSpecVersionStat(
            version='dont_use_me',
            support='a#',
        ))
