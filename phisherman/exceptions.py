class BasePhisermanException(Exception):
    ...


class InvalidRequest(BasePhisermanException):
    ...


class MissingPermission(BasePhisermanException):
    ...
