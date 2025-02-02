from os.path import exists as path_exists
from os import remove
import subprocess
from time import time
from typing import Tuple
from attributes import Attributes

from config import JAVA_CLASSPATH, TIMEOUT_MSSG
from results import PartialTestResult
from test_types import UnsupportedTestException
import mysql.connector


def parse_test(test):
    test_details = {}
    lines = test['code'].split('\n')
    for l in lines:
        broken = l.strip().split(':')
        if len(broken) == 2:
            test_details[broken[0].strip()] = broken[1].strip()
    return test_details


def run_script(timeout: float, database:str, filename:str):
    cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database=database)

    results = []
    stmts = open(filename).read().split(';')

    with cnx.cursor() as cursor:
        for stmt in stmts:
            if stmt.strip() != "":
                cursor.execute(stmt)
                results.append(cursor.fetchall())
    cnx.close()

    return results

def flatten(list_of_list_of_tuples_of_strings):
    o = ''
    for list_of_tuples_of_strings in list_of_list_of_tuples_of_strings:
        for tuple_of_strings in list_of_tuples_of_strings:
            for a_string in tuple_of_strings:
                o += str(a_string) + ', '
            o += '\n'
        o += '\n\n'
    return o

def run_sql_test(timeout: float, test: Attributes) -> Tuple[bool,str]:
    test_details = parse_test(test)
    run_script(timeout, '', test_details['setup'])
    actual = run_script(timeout, test_details['database'] , test['target'])
    expected = run_script(timeout, test_details['database'] , test_details['solution'])
    run_script(timeout, '', test_details['cleanup'])
    
    actual = flatten(actual)
    expected = flatten(expected)

    if (actual == expected):
        return True, ""
    
    else:
        out = "Expected : \n"
        out += expected
        out += "\n\nGot : \n"
        out += actual

        print(out)

        return False, out

def run_ddl_test(timeout: float, test: Attributes) -> Tuple[bool,str]:
    None

def run_test(test: Attributes) -> PartialTestResult:
    run_cmd = ["service", "mysql", "start"]
    p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        _, output_err = p.communicate(timeout=timeout)
        output = output_err.decode('utf-8')
    except subprocess.TimeoutExpired as e:
        output = TIMEOUT_MSSG
        exit("DB failed to start 1")
    except Exception as e:
        output = str(e)
        print(output)
        exit("DB failed to start 2")

    max_points = float(test['points'])
    runs = True
    point_multiplier = 100.0
    unapproved_includes = False
    sufficient_coverage = True
    timeout = float(test['timeout'])
    time_start = time()
    if test['type'] == 'sql':
        runs, run_output = run_sql_test(timeout, test)
    elif test['type'] == 'ddl':
        runs, run_output = run_ddl_test(timeout, test)
    else:
        # don't try to run an unsupported test
        raise UnsupportedTestException(test['type'])
    time_end = time()
    run_time = time_end - time_start

    if runs:
        if point_multiplier < 100.0:
            print(f"[PARTIAL PASS] ran partially correct and recieved {point_multiplier:0.2f}% partial credit\n")
        else:
            print('[PASS] ran correctly\n')
        points = max_points * (point_multiplier / 100.0)
    else:
        print('[FAIL] incorrect behavior\n')
        points = 0

    result: PartialTestResult = {
        'run_output': run_output,
        'unapproved_includes': unapproved_includes,
        'sufficient_coverage': sufficient_coverage,
        'points': points,
        'run_time': run_time
    }
    return result