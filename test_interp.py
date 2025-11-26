import subprocess
import shutil
import os
import re
import pytest

NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "input.nml.old"
#NML_PATH_2 = "input.new.nml"

WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"
EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf/work/model_mod_check"
#EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"


test_cases = [
    ((231.0, 40.0, 500.0), "QTY_POTENTIAL_TEMPERATURE"),
    ((250.0, 45.0, 1000.0), "QTY_U_WIND_COMPONENT"),
    ((260.0, 35.0, 2000.0), "QTY_V_WIND_COMPONENT"),
    ((240.0, 42.0, 1500.0), "QTY_SURFACE_PRESSURE"),
    ((235.0, 41.0, 800.0), "QTY_PRESSURE"),
    ((255.0, 44.0, 1200.0), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((245.0, 38.0, 600.0), "QTY_VERTICAL_VELOCITY"),
    ((232.0, 39.0, 400.0), "QTY_VAPOR_MIXING_RATIO"),
    ((250.0, 40.0, 500.0), "QTY_SURFACE_PRESSURE"),
]

def update_nml(nml_path, loc, qty):
    with open(nml_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if "loc_of_interest" in line:
            new_lines.append(f"   loc_of_interest       = {loc[0]}, {loc[1]}, {loc[2]}\n")
        elif "quantity_of_interest" in line:
            new_lines.append(f"   quantity_of_interest  = '{qty}'\n")
        else:
            new_lines.append(line)
    with open(nml_path, "w") as f:
        f.writelines(new_lines)

def run_model_mod_check(exe_path):
    result = subprocess.run(["mpirun", "-n", "4", exe_path], capture_output=True, text=True)
    return result

def extract_value(output, member=1):
    success_pattern = rf"member\s+{member}, SUCCESS with value\s+::\s+([0-9Ee\.\-]+)"
    match = re.search(success_pattern, output)
    if match:
        return float(match.group(1)), 'success'
    error_pattern = rf"member\s+{member}, ERROR with error code\s+::\s+([0-9Ee\.\-]+)"
    match = re.search(error_pattern, output)
    if match:
        error_code = int(float(match.group(1)))
        return error_code, 'error'
    raise ValueError("Neither SUCCESS value nor ERROR code found in output")

@pytest.fixture(scope="module", autouse=True)
def backup_restore_nml():
    if os.path.exists(WORK_NML_PATH):
        shutil.copyfile(WORK_NML_PATH, BACKUP_PATH)
    yield
    if os.path.exists(BACKUP_PATH):
        shutil.move(BACKUP_PATH, WORK_NML_PATH)

@pytest.mark.parametrize("loc,qty", test_cases)
def test_model_mod_check_equality(loc, qty):
    # Run v1
    shutil.copyfile(NML_PATH_1, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty)
    result1 = run_model_mod_check(EXE_PATH_1)
    assert result1.returncode == 0, f"model_mod_check_v1 failed: {result1.stderr}"
    value1, type1 = extract_value(result1.stdout)

    # Run v2
    shutil.copyfile(NML_PATH_2, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty)
    result2 = run_model_mod_check(EXE_PATH_2)
    assert result2.returncode == 0, f"model_mod_check_v2 failed: {result2.stderr}"
    value2, type2 = extract_value(result2.stdout)

    print(f"Value from v1: {value1} ({type1}), Value from v2: {value2} ({type2})")
    if type1 == 'error' and type2 == 'error':
        # Only require both to be errors, ignore error code
        assert True
    else:
        # Require both to be success and values to match
        assert value1 == value2 and type1 == type2, f"Values/type differ: {value1} ({type1}) != {value2} ({type2})"