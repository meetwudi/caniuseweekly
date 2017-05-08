import os
import tempfile
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import pytest

from caniuseweekly.cspec_loader import cspec_from_feature_json
from caniuseweekly.cspec_loader import feature_json_files
from testing.constants import EXAMPLE_FEATURE_JSON_PATH


def test_load_feature_json():
    with open(EXAMPLE_FEATURE_JSON_PATH, 'r') as f:
        cspec = cspec_from_feature_json(f.read())
        # some simple sanity checking
        assert cspec.title == 'CSS Grid Layout'
        assert len(cspec.bugs) == 2
        assert 'Method of using a grid' in cspec.description
        # stats is immutable
        with pytest.raises(Exception):
            cspec.stats['a'] = 1
        f.close()


def test_feature_json_files():
    filenames = ['feature1.json, feature2.json, feature3.json']
    with ExitStack() as stack:
        tempdir = tempfile.TemporaryDirectory()
        stack.enter_context(tempdir)
        stack.enter_context(mock.patch(
            'caniuseweekly.cspec_loader.source_repo_path',
            return_value=tempdir.name,
        ))
        os.mkdir(os.path.join(tempdir.name, 'features-json'))
        for filename in filenames:
            Path(os.path.join(tempdir.name, 'features-json', filename)).touch()
        assert feature_json_files() == filenames
