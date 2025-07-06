from logger import logger


@logger
def function_no_args():
    print(f"calling function_no_args")

@logger
def function_args(x, y):
    print(f"calling function_args({x}, {y})")
    return x + y

@logger
def function_calling_method():
    print(f"calling function_calling_method")
    function_no_args()

@logger
def function_failure():
    print(f"calling function_failure")
    2 / 0

@logger
def function_kwargs(param1=0, param2=0):
    print(f"calling function_kwargs(param1 = {param1}, param2 = {param2})")
    return param1 + param2

@logger
def function_args_kwargs(x, param3=0):
    print(f"calling function_args_kwargs(x, param3 = {param3})")
    return x + param3
