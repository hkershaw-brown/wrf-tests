import subprocess
import shutil
import os
import re
import pytest

NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "../../wrf/work/input.nml"
WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "./model_mod_check"
EXE_PATH_2 = "../../wrf/work/model_mod_check"

test_cases = [
    ((231.0, 40.0, 500.0), "QTY_POTENTIAL_TEMPERATURE"),
    # ... more cases ...
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
    pattern = rf"member\s+{member}, SUCCESS with value\s+::\s+([0-9Ee\.\-]+)"
    match = re.search(pattern, output)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("SUCCESS value not found in output")

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
    value1 = extract_value(result1.stdout)

    # Run v2
    shutil.copyfile(NML_PATH_2, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty)
    result2 = run_model_mod_check(EXE_PATH_2)
    assert result2.returncode == 0, f"model_mod_check_v2 failed: {result2.stderr}"
    value2 = extract_value(result2.stdout)

    print(f"Value from v1: {value1}, Value from v2: {value2}")
    assert value1 == value2, f"Values differ: {value1} != {value2}"