import functools
import os


def appconfig(name):
    def decorator(config_getter):
        override = None
        prefixed_name = 'caniuseweekly_{}'.format(name)

        if prefixed_name in os.environ:
            # override from environment variable
            override = os.environ[prefixed_name]

        @functools.wraps(config_getter)
        def wrapper():
            # return hard-coded config value if no override happens
            return override if override else config_getter()
        return wrapper
    return decorator
