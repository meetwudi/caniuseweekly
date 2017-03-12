import attr


class DictValidatorKeypathDoesNotExistError(Exception):
    pass


@attr.s
class _DictValidator():
    required_keypaths = attr.ib(validator=attr.validators.instance_of(list))

    def __call__(self, inst, attr, value):
        if not isinstance(value, dict):
            raise TypeError(
                "'{name}' must be a dict object.".format(
                    name=attr.name,
                ),
            )

        if not self.required_keypaths:
            return

        for keypath in self.required_keypaths:
            current = value
            components = keypath.split('.')
            for component in components[:-1]:
                current = current.get(component, {})
            if components[-1] not in current:
                raise DictValidatorKeypathDoesNotExistError(
                    "'{keypath}' not found".format(
                        keypath=keypath,
                    )
                )


def dict_validator(required_keypaths):
    return _DictValidator(required_keypaths)
