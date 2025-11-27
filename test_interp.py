import subprocess
import shutil
import os
import re
import pytest

NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "input.old.nml"
#NML_PATH_2 = "input.new.nml"

WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"
EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf/work/model_mod_check"
#EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"

test_cases = [
    ((1.477, 45.237, 7451.7), "QTY_VERTICAL_VELOCITY"),
    ((359.904, 43.668, 8921.9), "QTY_POTENTIAL_TEMPERATURE"),
    ((359.995, 43.434, 7017.4), "QTY_V_WIND_COMPONENT"),
    ((0.102, 45.764, 8847.0), "QTY_PRESSURE"),
    ((0.475, 45.086, 7070.4), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.913, 43.885, 8930.7), "QTY_QVAPOR"),
    ((1.238, 44.065, 7451.3), "QTY_PRESSURE"),
    ((2.315, 46.118, 7205.7), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((2.215, 45.113, 8775.3), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((1.978, 43.516, 7921.2), "QTY_PRESSURE"),
    ((359.705, 45.189, 8078.4), "QTY_V_WIND_COMPONENT"),
    ((1.111, 43.995, 8660.8), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.013, 45.366, 8095.3), "QTY_V_WIND_COMPONENT"),
    ((0.816, 44.167, 7263.5), "QTY_V_WIND_COMPONENT"),
    ((1.109, 43.948, 7799.4), "QTY_U_WIND_COMPONENT"),
    ((0.655, 44.076, 7447.5), "QTY_QVAPOR"),
    ((0.773, 45.089, 7383.0), "QTY_QVAPOR"),
    ((1.434, 45.051, 7598.1), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((1.707, 44.306, 8277.6), "QTY_QVAPOR"),
    ((359.052, 44.190, 8757.8), "QTY_PRESSURE"),
    ((358.798, 44.030, 8601.2), "QTY_VERTICAL_VELOCITY"),
    ((1.046, 45.001, 8872.4), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.150, 44.751, 8933.7), "QTY_QVAPOR"),
    ((358.400, 44.571, 8344.8), "QTY_PRESSURE"),
    ((359.547, 44.060, 8884.8), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.500, 43.952, 8581.2), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.887, 43.688, 7790.2), "QTY_QVAPOR"),
    ((1.077, 43.469, 7384.7), "QTY_POTENTIAL_TEMPERATURE"),
    ((357.940, 44.933, 7219.3), "QTY_U_WIND_COMPONENT"),
    ((1.504, 43.565, 8691.0), "QTY_PRESSURE"),
    ((358.957, 46.684, 8538.3), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.001, 45.412, 8024.3), "QTY_PRESSURE"),
    ((1.863, 46.099, 7442.4), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.882, 43.679, 7197.3), "QTY_QVAPOR"),
    ((358.827, 43.736, 8886.2), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.138, 44.736, 7790.2), "QTY_U_WIND_COMPONENT"),
    ((358.751, 43.540, 8607.3), "QTY_POTENTIAL_TEMPERATURE"),
    ((0.812, 44.594, 7096.8), "QTY_PRESSURE"),
    ((1.791, 45.371, 8810.7), "QTY_VERTICAL_VELOCITY"),
    ((0.152, 44.655, 7980.6), "QTY_VERTICAL_VELOCITY"),
    ((0.940, 44.348, 8375.4), "QTY_U_WIND_COMPONENT"),
    ((1.655, 45.859, 8081.2), "QTY_PRESSURE"),
    ((1.676, 44.936, 8390.6), "QTY_V_WIND_COMPONENT"),
    ((1.475, 43.631, 8482.0), "QTY_QVAPOR"),
    ((1.206, 43.861, 7327.0), "QTY_POTENTIAL_TEMPERATURE"),
    ((0.500, 44.968, 7472.5), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.708, 43.927, 7542.7), "QTY_POTENTIAL_TEMPERATURE"),
    ((359.943, 43.694, 8842.2), "QTY_V_WIND_COMPONENT"),
    ((359.517, 44.165, 8662.2), "QTY_V_WIND_COMPONENT"),
    ((357.871, 46.429, 7105.1), "QTY_POTENTIAL_TEMPERATURE"),
    ((359.992, 43.545, 8074.8), "QTY_VERTICAL_VELOCITY"),
    ((358.031, 45.114, 7305.3), "QTY_VERTICAL_VELOCITY"),
    ((0.675, 45.248, 8969.0), "QTY_QVAPOR"),
    ((359.036, 44.665, 7203.3), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.576, 43.249, 7257.2), "QTY_QVAPOR"),
    ((1.204, 43.407, 8084.1), "QTY_PRESSURE"),
    ((0.060, 44.176, 8553.5), "QTY_V_WIND_COMPONENT"),
    ((0.777, 43.538, 8701.5), "QTY_VERTICAL_VELOCITY"),
    ((358.441, 44.747, 7235.6), "QTY_VERTICAL_VELOCITY"),
    ((358.168, 45.789, 8158.9), "QTY_V_WIND_COMPONENT"),
    ((358.994, 43.741, 7806.8), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.636, 43.453, 7533.4), "QTY_QVAPOR"),
    ((358.639, 46.262, 8939.4), "QTY_PRESSURE"),
    ((2.097, 43.761, 7971.9), "QTY_V_WIND_COMPONENT"),
    ((359.823, 44.356, 7405.6), "QTY_U_WIND_COMPONENT"),
    ((0.317, 44.961, 8144.5), "QTY_U_WIND_COMPONENT"),
    ((358.904, 44.066, 8219.5), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((0.211, 43.706, 8689.2), "QTY_U_WIND_COMPONENT"),
    ((0.245, 44.454, 8054.0), "QTY_V_WIND_COMPONENT"),
    ((358.256, 46.548, 8969.8), "QTY_VERTICAL_VELOCITY"),
    ((0.136, 44.462, 7088.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.486, 44.396, 7019.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((0.105, 44.627, 8591.2), "QTY_PRESSURE"),
    ((357.917, 45.634, 8059.6), "QTY_U_WIND_COMPONENT"),
    ((0.116, 44.336, 7651.3), "QTY_PRESSURE"),
    ((358.106, 44.651, 7740.2), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((2.096, 46.155, 7940.3), "QTY_VERTICAL_VELOCITY"),
    ((358.970, 46.357, 7604.8), "QTY_VERTICAL_VELOCITY"),
    ((358.250, 46.160, 8368.0), "QTY_U_WIND_COMPONENT"),
    ((1.245, 45.411, 7814.4), "QTY_PRESSURE"),
    ((359.615, 43.614, 7324.5), "QTY_V_WIND_COMPONENT"),
    ((359.804, 44.278, 7406.0), "QTY_V_WIND_COMPONENT"),
    ((359.205, 45.115, 8342.5), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.202, 44.451, 8827.0), "QTY_V_WIND_COMPONENT"),
    ((359.069, 43.575, 7435.8), "QTY_V_WIND_COMPONENT"),
    ((0.631, 44.424, 7799.1), "QTY_U_WIND_COMPONENT"),
    ((358.110, 45.593, 8198.2), "QTY_QVAPOR"),
    ((0.401, 43.284, 7010.5), "QTY_V_WIND_COMPONENT"),
    ((1.881, 44.556, 8868.0), "QTY_U_WIND_COMPONENT"),
    ((0.530, 44.920, 7355.9), "QTY_VERTICAL_VELOCITY"),
    ((358.959, 45.349, 7164.4), "QTY_PRESSURE"),
    ((359.151, 44.414, 8320.1), "QTY_U_WIND_COMPONENT"),
    ((1.194, 45.193, 7720.3), "QTY_PRESSURE"),
    ((359.165, 43.543, 8802.5), "QTY_VERTICAL_VELOCITY"),
    ((1.516, 46.350, 7153.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.473, 45.112, 7464.8), "QTY_PRESSURE"),
    ((0.941, 44.971, 7328.3), "QTY_V_WIND_COMPONENT"),
    ((1.382, 45.795, 7064.6), "QTY_VERTICAL_VELOCITY"),
    ((358.375, 44.087, 8427.9), "QTY_U_WIND_COMPONENT"),
    ((0.783, 44.932, 7642.1), "QTY_POTENTIAL_TEMPERATURE"),
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
        print(f"Found ERROR with code: {error_code}")
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