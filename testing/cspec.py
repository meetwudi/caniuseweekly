import os

from caniuseweekly.cspec_loader import cspec_from_feature_json
from testing.constants import FIXTURES_FOLDER_PATH

def fake_cspec_from_fixture(id='default'):
    fixture_path = os.path.join(
        FIXTURES_FOLDER_PATH,
        'example-feature-json-{}.json'.format(id),
    )
    with open(fixture_path, 'r') as fp:
        return cspec_from_feature_json(fp.read())
