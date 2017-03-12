import attr

from caniuseweekly.browser import Browser


@attr.s
class CSpec():
    """A Caniuse Specification of a browser. An CSpec would include features supported by a certain browser according to Caniuse.com.
    """
    browser = attr.ib(validator=attr.validators.instance_of(Browser))
