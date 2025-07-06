from src.sample_class import *


class TestClass:
    
    obj: SampleClass = None

    def test_01_init(self):
        TestClass.obj = SampleClass(0)

    def test_02_no_args(self):
        TestClass.obj.method_no_args()

    def test_03_args(self):
        TestClass.obj.method_args(1, 2)

    def test_04_call(self):
        TestClass.obj.method_calling_method()

    def test_05_fail(self):
        TestClass.obj.method_failure()

    def test_06_kwargs(self):
        TestClass.obj.method_kwargs(param2=4, param1=3)

    def test_07_kwargs(self):
        TestClass.obj.method_kwargs(param2=4)

    def test_08_args_kwargs(self):
        TestClass.obj.method_args_kwargs(5, param3=6)

    def test_09_staticmethod(self):
        SampleClass.method_static(2, 3)

    def test_10_classmethod(self):
        SampleClass.method_class(3)
    