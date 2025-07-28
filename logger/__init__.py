import base64
import importlib
import inspect
import logging
import os
import types
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
            if classify_callable(func) in ("method", "class_method", "property"):
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


def classify_callable(func) -> str:
    """
    Given a function object (with __module__ and __qualname__), classify it as one of:
    - 'method'
    - 'class_method'
    - 'static_method'
    - 'nested_function'
    - 'function'
    - 'property'
    """
    mod = importlib.import_module(func.__module__)
    parts = func.__qualname__.split('.')

    if '<locals>' in func.__qualname__:
        return 'nested_function'

    try:
        # Step 1: Load module and walk to object
        obj = mod
        for part in parts[:-1]:
            obj = getattr(obj, part)
        class_or_scope = obj
        attr_name = parts[-1]

        # Step 2: Get raw attribute without invoking descriptor logic
        raw_attr = inspect.getattr_static(class_or_scope, attr_name)

        # Step 3: Inspect the type of descriptor
        if isinstance(raw_attr, staticmethod):
            return 'static_method'
        elif isinstance(raw_attr, classmethod):
            return 'class_method'
        elif isinstance(raw_attr, property):
            return 'property'
        elif (
            isinstance(raw_attr, types.FunctionType)
            and '.' not in func.__qualname__
        ):
            return 'function'
        elif inspect.isfunction(raw_attr):
            return 'method'
        else:
            return 'unknown'
    except Exception:
        return 'unknown'


def is_self_parameter(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    if not params:
        return False
    return params[0].name == "self"


def is_classmethod(func):
    mod = importlib.import_module(func.__module__)
    parts = func.__qualname__.split('.')

    attr_name = parts[-1]
    class_path = parts[:-1]

    obj = mod
    for part in class_path:
        obj = getattr(obj, part)
    cls = obj  # now obj should be the class
    try:
        attr = inspect.getattr_static(cls, attr_name)
        return isinstance(attr, classmethod)
    except AttributeError:
        return False


def is_bound_instance_method(func) -> bool:
    """
    Given the __module__ and __qualname__ of a function, determine if it is:
    - an instance method (i.e., of type `method`)
    - bound to a class (not just a free function)
    """
    try:
        # Step 1: Load the object
        mod = importlib.import_module(func.__module__)
        parts = func.__qualname__.split('.')

        # Step 2: Walk down to the object
        obj = mod
        for part in parts:
            obj = getattr(obj, part)

        # Step 3: Validate it's a bound method
        if isinstance(obj, types.MethodType):
            # Check if it’s bound to a class (not a plain instance or None)
            self_obj = obj.__self__
            return not inspect.isclass(self_obj)
        else:
            return False

    except (AttributeError, ImportError):
        return False


def resolve_qualname(module_name, qualname):
    mod = importlib.import_module(module_name)
    obj = mod
    for part in qualname.split('.'):
        obj = getattr(obj, part)
    return obj


def get_type(module_name, qualname):
    mod = importlib.import_module(module_name)
    parts = qualname.split('.')

    attr_name = parts[-1]
    class_path = parts[:-1]

    obj = mod
    for part in class_path:
        obj = getattr(obj, part)
    try:
        attr = inspect.getattr_static(obj, attr_name)
        return type(attr)
    except AttributeError:
        return None
