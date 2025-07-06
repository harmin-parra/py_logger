import base64
import importlib
import inspect
import logging
import os
from functools import wraps


DEBUG = False
LEVEL = 60
TRUNCATE = 500


nested_calls = -1
exiting = False


if 'PYTEST_LOGGER' in os.environ.keys() and os.environ['PYTEST_LOGGER'].lower() == 'true':
    DEBUG = True


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DEBUG:
            global nested_calls, exiting
            nested_calls = nested_calls + 1 if nested_calls >= 0 else 0
            indent = ' ' * 2 * nested_calls
            if nested_calls != 0 and not exiting:
                logging.log(LEVEL, '')
            exiting = False
            logging.log(LEVEL, "%sCALLING %s.%s", indent, func.__module__, func.__qualname__)
            if (
                is_self_parameter(func) or
                str(type(resolve_qualname(func.__module__, func.__qualname__))) == "<class 'method'>"
            ):
                temp_args = args[1:]
            else:
                temp_args = args
            params = []
            for value in temp_args:
                params.append(truncate(value))
            for key, value in kwargs.items():
                params.append("{} = {}".format(key, truncate(value)))
            if len(params) > 0:
                logging.log(LEVEL, "%sARGUMENTS: %s", indent, params)
            try:
                resp = func(*args, **kwargs)
                if resp is not None:
                    logging.log(LEVEL, "%sRETURNING: %s", indent, truncate(resp))
                logging.log(LEVEL, "%sEXITING %s.%s", indent, func.__module__, func.__qualname__)
                logging.log(LEVEL, '')
                exiting = True
                nested_calls = nested_calls - 1
                return resp
            except Exception as error:
                logging.log(LEVEL, "%sTHROWING %s", indent, repr(error))
                logging.log(LEVEL, "%sEXITING %s.%s", indent, func.__module__, func.__qualname__)
                logging.log(LEVEL, '')
                exiting = True
                nested_calls = nested_calls - 1
                raise error
        else:
            return func(*args, **kwargs)
    return wrapper


def truncate(value):
    if isinstance(value, bytes):
        value = base64.b64encode(value).decode()
    if len(repr(value)) > TRUNCATE:
        return repr(value)[:TRUNCATE] + "...."
    else:
        return repr(value)


def is_self_parameter(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    if not params:
        return None
    return params[0].name == "self"


def resolve_qualname(module_name, qualname):
    mod = importlib.import_module(module_name)
    obj = mod
    for part in qualname.split('.'):
        obj = getattr(obj, part)
    return obj
