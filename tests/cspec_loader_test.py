from caniuseweekly.cspec_loader import cspec_from_feature_json
from testing.constants import EXAMPLE_FEATURE_JSON_PATH


def test_load_feature_json():
    with open(EXAMPLE_FEATURE_JSON_PATH, 'r') as f:
        cspec = cspec_from_feature_json(f.read())
        # some simple sanity checking
        assert cspec.title == 'CSS Grid Layout'
        assert len(cspec.bugs) == 2
        assert 'Method of using a grid' in cspec.description
        f.close()
