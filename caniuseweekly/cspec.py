import enum

import attr

from caniuseweekly.browser import Browser
from caniuseweekly.cspec_diff import CSpecDiff
from caniuseweekly.validators import dict_validator


@enum.unique
class CSpecStatus(enum.Enum):
    LS = 'WHATWG Living Standard'
    REC = 'W3C Recommendation'
    PR = 'W3C Proposed Recommendation'
    CR = 'W3C Candidate Recommendation'
    WD = 'W3C Working Draft'
    OTHER = 'Non-W3C, but reputable'
    UNOFF = 'Unofficial, Editor\'s Draft or W3C "Note"'


@enum.unique
class CSpecCategory(enum.Enum):
    HTML5 = 'HTML5'
    CSS = 'CSS'
    CSS2 = 'CSS2'
    CSS3 = 'CSS3'
    SVG = 'SVG'
    PNG = 'PNG'
    JS_API = 'JavaScript API'
    CANVAS = 'Canvas'
    DOM = 'DOM'
    OTHER = 'Other'


@enum.unique
class CSpecStat(enum.Enum):
    Y = 'Supported by default'
    A = 'Almost supported'
    N = 'No support'
    P = 'No support, but has Polyfill'
    U = 'Support unknown'
    X = 'Requires prefix to work'
    D = 'Disabled by default'


@attr.s
class CSpec():
    """A Caniuse Specification of a feature.
    """
    bugs = attr.ib(validator=attr.validators.instance_of(list))
    categories = attr.ib(validator=attr.validators.instance_of(list))
    description = attr.ib(validator=attr.validators.instance_of(str))
    spec = attr.ib(validator=attr.validators.instance_of(str))
    stats = attr.ib(validator=dict_validator(
        Browser.all_code_friendly_names()))
    title = attr.ib(validator=attr.validators.instance_of(str))

    def __sub__(self, other):
        return CSpecDiff.create(self, other)
