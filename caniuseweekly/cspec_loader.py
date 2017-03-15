import json

from caniuseweekly.cspec import CSpec


def cspec_from_feature_json(feature_json):
    """Create a CSpec instance from feature_json string.

    :param feature_json: JSON string of Caniuse feature json
    """
    raw = json.loads(feature_json)
    cspec_kwargs = {}

    direct_mapping_names = [
        'bugs',
        'categories',
        'description',
        'spec',
        'stats',
        'title',
    ]
    for key in direct_mapping_names:
        cspec_kwargs[key] = raw[key]

    return CSpec(**cspec_kwargs)
