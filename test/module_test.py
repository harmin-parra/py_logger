from src.sample_module import *


def test_1_no_args():
    function_no_args()

def test_2_args():
    function_args(1, 2)

def test_3_call():
    function_calling_method()

def test_4_fail():
    function_failure()

def test_5_kwargs():
    function_kwargs(param2=4, param1=3)

def test_6_kwargs():
    function_kwargs(param2=4)

def test_7_args():
    function_args_kwargs(5, param3=6)
