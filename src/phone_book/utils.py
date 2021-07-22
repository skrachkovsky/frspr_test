import typing
from importlib import import_module

__all__ = 'load_object', 'load_module'


def load_object(string_name: str, raise_error: bool = True):
    objname = string_name.split('.')
    if objname and len(objname) > 1:
        mod = import_module('.'.join(objname[:-1]), objname[-1])
        return getattr(mod, objname[-1])
    if raise_error:
        raise ImportError('Loading class %s filed' % string_name)


def load_module(string_name: str, raise_error: bool = True) -> typing.Any:
    return import_module(string_name)
