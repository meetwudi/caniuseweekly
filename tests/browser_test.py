from caniuseweekly.browser import Browser
from caniuseweekly.browser import BrowserName


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
    ] == Browser.all_code_friendly_names()


def test_from_code_friendly_name():
    code_friendly_name = 'chrome'
    browser = Browser.from_code_friendly_name(code_friendly_name)
    assert browser.name is BrowserName.CHROME
