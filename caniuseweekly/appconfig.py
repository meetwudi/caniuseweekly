import functools
import os


def appconfig(config_getter):
    override = None
    prefixed_name = 'caniuseweekly_{}'.format(config_getter.__name__)

    if prefixed_name in os.environ:
        # override from environment variable
        override = os.environ[prefixed_name]

    @functools.wraps(config_getter)
    def wrapper():
        # return hard-coded config value if no override happens
        return override if override else config_getter()
    return wrapper
