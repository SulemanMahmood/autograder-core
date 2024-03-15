from attributes import Attributes
from test_types import UnsupportedTestException

def write_unit_test(test: Attributes) -> None:
    with open('UnitTest.hs', 'wt') as f:
        # Import HUnit library and potentially other necessary imports based on `test`
        f.write('import Test.HUnit\n')
        f.write('import System.Exit (exitFailure, exitSuccess)\n\n')

        # Dynamically generate test case based on `test` attributes
        functionName = test.function_name  # This is a hypothetical attribute
        inputValue = test.input_value  # Hypothetical attribute
        expectedValue = test.expected_value  # Hypothetical attribute
        f.write(f'test1 = TestCase (assertEqual "for ({functionName})," {expectedValue} ({functionName} {inputValue}))\n\n')

        # Test list and main function to run tests
        f.write('tests = TestList [ TestLabel "test1" test1 ]\n\n')
        f.write('main = do\n')
        f.write('  results <- runTestTT tests\n')
        f.write('  if errors results + failures results == 0\n')
        f.write('    then exitSuccess\n')
        f.write('    else exitFailure\n')



def write_performance_test_haskell(test: Attributes) -> None:
    with open('PerformanceTest.hs', 'wt') as f:
        # Haskell module header and imports
        f.write('module PerformanceTest where\n')
        f.write('import System.CPUTime\n')
        f.write('import Text.Printf\n\n')
        
        # Main function and performance measurement
        f.write('main :: IO ()\n')
        f.write('main = do\n')
        f.write('  start <- getCPUTime\n')
        f.write('  {}\n'.format('\n  '.join(test['code'].splitlines())))
        f.write('  end <- getCPUTime\n')
        f.write('  let diff = (fromIntegral (end - start)) / (10^12)\n')
        f.write('  printf "operation took %0.3f sec\\n" (diff :: Double)\n')

# Writes out the input and output strings
def write_io_test(test: Attributes) -> None:
    with open('input.txt', 'wt') as f:
        f.write(test['expected_input'])
        f.write("\n")
    with open('output.txt', 'wt') as f:
        f.write(test['expected_output'])

def write_script_test(test: Attributes) -> None:
    with open('script.sh', 'wt') as f:
        f.write(test['script_content'])

def write_approved_includes_test(test: Attributes) -> None:
    test['script_content'] = f"./approved_includes.sh {test['target']} {' '.join(test['approved_includes'])}"
    write_script_test(test)

def write_coverage_test(test: Attributes) -> None:
    test['script_content'] = f"./coverage.sh {test['target']} {test['include']} {' '.join(test['approved_includes'])}"
    write_script_test(test)

def write_compile_test(test: Attributes) -> None:
    test['script_content'] = f"./compiles.sh {' '.join(test['approved_includes'])}"
    write_script_test(test)

def write_style_test(test: Attributes) -> None:
    test['script_content'] = f"./check_style.sh {' '.join(test['approved_includes'])}"
    write_script_test(test)

def write_test(test: Attributes) -> None:
    if test['type'] == 'unit':
        write_unit_test(test)
    elif test['type'] == 'i/o':
        write_io_test(test)
    elif test['type'] == 'script':
        write_script_test(test)
    elif test['type'] == 'approved_includes':
        write_approved_includes_test(test)
    elif test['type'] == 'performance':
        write_performance_test_haskell(test)
    elif test['type'] == 'coverage':
        write_coverage_test(test)
    elif test['type'] == 'compile':
        write_compile_test(test)
    elif test['type'] == 'style':
        write_style_test(test)
    else:
        # don't try to write an unsupported test
        raise UnsupportedTestException(test['type'])