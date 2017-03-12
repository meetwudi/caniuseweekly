import enum

import attr


@attr.s
class BrowserNameValue():
    code_friendly_name = attr.ib(validator=attr.validators.instance_of(str))
    display_name = attr.ib(validator=attr.validators.instance_of(str))


@enum.unique
class BrowserName(enum.Enum):
    CHROME = BrowserNameValue(
        code_friendly_name='chrome', display_name='Chrome')
    EDGE = BrowserNameValue(code_friendly_name='edge', display_name='IE Edge')
    IE = BrowserNameValue(code_friendly_name='ie',
                          display_name='Internet Explorer')
    FIREFOX = BrowserNameValue(
        code_friendly_name='firefox', display_name='Firefox')
    SAFARI = BrowserNameValue(
        code_friendly_name='safari', display_name='Safari')
    OPERA = BrowserNameValue(code_friendly_name='opera', display_name='Opera')
    SAFARI_MOBILE = BrowserNameValue(
        code_friendly_name='ios_saf', display_name='iOS Safari')
    ANDROID = BrowserNameValue(
        code_friendly_name='android', display_name='Android')

    @classmethod
    def all_code_friendly_names(cls):
        return [browser_name.value.code_friendly_name for browser_name in cls]


@attr.s
class Browser():
    """Represents a browser.
    """
    name = attr.ib(attr.validators.instance_of(BrowserName))
