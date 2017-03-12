from caniuseweekly.browser import BrowserName
from caniuseweekly.browser import Browser


def test_all_code_friendly_names():
    assert [
        'chrome',
        'edge',
        'ie',
        'firefox',
        'safari',
        'opera',
        'ios_saf',
        'android',
    ] == BrowserName.all_code_friendly_names()
