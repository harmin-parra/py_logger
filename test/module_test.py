from src import sample_module


def test_1_no_args():
    sample_module.function_no_args()

def test_2_args():
    sample_module.function_args(1, 2)

def test_3_call():
    sample_module.function_calling_method()

def test_4_fail():
    sample_module.function_failure()

def test_5_kwargs():
    sample_module.function_kwargs(param2=4, param1=3)

def test_6_kwargs():
    sample_module.function_kwargs(param2=4)

def test_7_args():
    sample_module.function_args_kwargs(5, param3=6)
