from typing import List, Tuple
from os import popen

# Assuming similar structure for Attributes, but adapted for Haskell environment
from attributes import Attributes
from config import GHC_PATH, GHC_FLAGS
from test_types import UnsupportedTestException

def compile_hs_test(src: List[str]) -> Tuple[bool, str]:
    SRC = ' '.join(src)

    compile_cmd = '{} {} {} 2>&1'.format(GHC_PATH, GHC_FLAGS, SRC)
    p = popen(compile_cmd)
    try:
        output = p.read()
    except Exception as e:
        output = str(e)
    ret = p.close()
    return ret is None, output

def compile_unit_test(src: List[str]) -> Tuple[bool, str]:
    return compile_hs_test(src + ['UnitTest.hs', 'UnitTestRunner.hs', 'TestRunner.hs'])

def compile_performance_test(src: List[str]) -> Tuple[bool, str]:
    return compile_hs_test(src + ['PerformanceTest.hs'])

def compile_io_test(src: List[str]) -> Tuple[bool, str]:
    return compile_hs_test(src)

def compile_script_test() -> Tuple[bool, str]:
    # Assuming no compilation needed for scripts in Haskell or handled differently
    return True, ""

def compile_approved_includes_test() -> Tuple[bool, str]:
    # Assuming checks for approved includes might differ for Haskell
    return True, ""

def compile_coverage_test() -> Tuple[bool, str]:
    # Assuming coverage testing is handled differently for Haskell
    return True, ""

def compile_compile_test() -> Tuple[bool, str]:
    # This function might be redundant for Haskell if all compilation is handled uniformly
    return True, ""

def compile_style_test() -> Tuple[bool, str]:
    # Assuming style checks are handled differently or not applicable in the same way for Haskell
    return True, ""

def compile_test(test: Attributes) -> Tuple[bool, str]:
    compiles = False
    compile_output = ''
    if test['type'] == 'unit':
        compiles, compile_output = compile_unit_test([test['target'], test['include']])
    elif test['type'] == 'i/o':
        compiles, compile_output = compile_io_test([test['target'], test['include']])
    elif test['type'] == 'script':
        compiles, compile_output = compile_script_test()
    elif test['type'] == 'performance':
        compiles, compile_output = compile_performance_test([test['target'], test['include']])
    elif test['type'] == 'approved_includes':
        compiles, compile_output = compile_approved_includes_test()
    elif test['type'] == 'coverage':
        compiles, compile_output = compile_coverage_test()
    elif test['type'] == 'compile':
        compiles, compile_output = compile_compile_test()
    elif test['type'] == 'style':
        compiles, compile_output = compile_style_test()
    else:
        # don't try to compile an unsupported test
        raise UnsupportedTestException(test['type'])
    return compiles, compile_output

# Example of updated config variables (in config.py)
GHC_PATH = "ghc"
GHC_FLAGS = "-Wall"  # Example GHC flags, adjust as needed
