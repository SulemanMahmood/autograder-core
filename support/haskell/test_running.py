from os.path import exists as path_exists
from os import remove
import subprocess
from time import time
from typing import Tuple

# Assuming similar configuration and utility files exist for Haskell environment setup
from config import HASKELL_COMPILER, HASKELL_RUNNER, TIMEOUT_MSSG
from results import PartialTestResult
from test_types import UnsupportedTestException

def remove_end_of_line_whitespace(s: str) -> str:
    lines = s.split('\n')
    lines = [line.rstrip() for line in lines]
    return '\n'.join(lines)

def base_name(filename):
    # convert "Code.hs" -> "Code"
    return filename[:-3]

def compile_haskell(source_name: str) -> bool:
    compile_cmd = [HASKELL_COMPILER, source_name, "-o", base_name(source_name)]
    compilation_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return compilation_result.returncode == 0

def run_code(executable_name: str, timeout: float) -> Tuple[bool, str]:
    if not compile_haskell(executable_name + '.hs'):
        return False, "Compilation failed."
    
    run_cmd = ["./" + executable_name]
    try:
        process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_bytes, _ = process.communicate(timeout=timeout)
        output = output_bytes.decode('utf-8')
    except subprocess.TimeoutExpired:
        output = TIMEOUT_MSSG
    except Exception as e:
        output = str(e)
    return process.returncode == 0, output

def run_io_test(timeout: float, main: str) -> Tuple[bool,str]:
    executable_name = base_name(main)
    # Input/output file handling remains the same
    # ...

def run_script_test(timeout: float, args: str = '') -> Tuple[bool,str,float]:
    # Adjusted for Haskell, if necessary
    # ...

# Adapt other test running functions similarly

def run_test(test) -> PartialTestResult:
    # This function's logic remains mostly unchanged, but ensure it calls the Haskell-adjusted functions
    # ...

# Example configuration (config.py adjustments)
HASKELL_COMPILER = "ghc"
HASKELL_RUNNER = ""  # Not used since running is done directly on the compiled output

