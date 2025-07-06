from logger import logger


class SampleClass:

    @logger
    def __init__(self, x):
        self.x = x
        print(f"calling __init__({x})")

    @logger
    def method_no_args(self):
        print("calling method_no_args")

    @logger
    def method_args(self, x, y):
        print(f"calling method_args({x}, {y})")
        return x + y

    @logger
    def method_calling_method(self):
        print("calling method_calling_method")
        self.method_no_args()

    @logger
    def method_failure(self):
        print("calling method_failure")
        2 / 0

    @logger
    def method_kwargs(self, param1=0, param2=0):
        print(f"calling method_kwargs(param1 = {param1}, param2 = {param2})")
        return param1 + param2

    @logger
    def method_args_kwargs(self, x, param3=0):
        print(f"calling method_args_kwargs({x}, param3 = {param3})")
        return x + param3
    
    @staticmethod
    @logger
    def method_static(x, y):
        print(f"calling method_static({x}, {y})")
        return x + y
    
    @classmethod
    @logger
    def method_class(cls, x):
        print(f"calling method_class({x})")
        return cls(x)
