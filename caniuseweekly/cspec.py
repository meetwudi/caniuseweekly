import attr
import enum

from caniuseweekly.browser import Browser

@enum.unique
class CSpecStatus():
    LS = 'WHATWG Living Standard'
    REC = 'W3C Recommendation'
    PR = 'W3C Proposed Recommendation'
    CR = 'W3C Candidate Recommendation'
    WD = 'W3C Working Draft'
    OTHER = 'Non-W3C, but reputable'
    UNOFF = 'Unofficial, Editor\'s Draft or W3C "Note"'


@attr.s
class CSpec():
    """A Caniuse Specification of a browser. An CSpec would include features
    supported by a certain browser according to Caniuse.com.
    """
    browser = attr.ib(validator=attr.validators.instance_of(Browser))
    description = attr.ib(validator=attr.validators.instance_of(str))
    spec_url = attr.ib(validator=attr.validators.instance_of(str))
    title = attr.ib(validator=attr.validators.instance_of(str))
