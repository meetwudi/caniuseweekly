from typing import NamedTuple

CSpecVersionStat = NamedTuple('CSpecVersionStat', [
    ('version', str),
    ('support', str),
])


def note_num_from_version_stat(cspec_version_stat):
    if '#' in cspec_version_stat.support:
        return int(cspec_version_stat.support.split('#')[1].strip())
    return None
