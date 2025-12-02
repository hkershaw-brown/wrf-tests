import subprocess
import shutil
import os
import re
import pytest

# currently hand setting vertiscal coordinate to use in input.X.nml
NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "input.old.nml"
#NML_PATH_2 = "input.new.nml"

WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"
EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf/work/model_mod_check"
#EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"

test_cases = [
    ((357.764, 43.318, 90798.7), "QTY_POTENTIAL_TEMPERATURE"),
    ((359.339, 44.003, 88000.5), "QTY_U_WIND_COMPONENT"),
    ((359.387, 43.514, 68813.0), "QTY_U_WIND_COMPONENT"),
    ((359.172, 44.196, 63227.7), "QTY_U_WIND_COMPONENT"),
    ((0.243, 44.621, 74618.2), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((1.428, 43.880, 72275.8), "QTY_2M_TEMPERATURE"),
    ((359.636, 44.179, 77854.4), "QTY_CONDENSATIONAL_HEATING"),
    ((358.230, 46.756, 76556.8), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((358.770, 44.111, 78527.5), "QTY_SURFACE_ELEVATION"),
    ((357.906, 43.945, 84562.0), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((358.571, 44.051, 71722.6), "QTY_V_WIND_COMPONENT"),
    ((1.812, 46.600, 93165.4), "QTY_U10_WIND_COMPONENT"),
    ((2.317, 43.382, 68038.2), "QTY_RAIN_NUMBER_CONCENTR"),
    ((359.610, 43.923, 75247.7), "QTY_RAIN_NUMBER_CONCENTR"),
    ((1.258, 45.384, 95383.2), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((358.882, 43.831, 58650.1), "QTY_CONDENSATIONAL_HEATING"),
    ((0.207, 43.885, 85284.3), "QTY_SKIN_TEMPERATURE"),
    ((0.488, 43.490, 62493.2), "QTY_SURFACE_PRESSURE"),
    ((359.635, 43.808, 80618.1), "QTY_PRESSURE"),
    ((1.806, 45.151, 53032.4), "QTY_VAPOR_MIXING_RATIO"),
    ((0.731, 43.284, 98008.3), "QTY_PRESSURE"),
    ((359.111, 45.836, 84407.2), "QTY_U_WIND_COMPONENT"),
    ((1.712, 45.119, 52789.9), "QTY_RADAR_REFLECTIVITY"),
    ((1.212, 44.215, 84985.2), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.483, 44.179, 58982.5), "QTY_LANDMASK"),
    ((2.390, 45.971, 64532.9), "QTY_SKIN_TEMPERATURE"),
    ((1.346, 46.387, 77619.0), "QTY_RADAR_REFLECTIVITY"),
    ((357.879, 46.476, 91818.3), "QTY_RADAR_REFLECTIVITY"),
    ((359.003, 45.137, 51822.4), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((1.487, 43.765, 68044.1), "QTY_CONDENSATIONAL_HEATING"),
    ((0.868, 44.843, 96161.3), "QTY_VERTICAL_VELOCITY"),
    ((358.182, 44.346, 98142.7), "QTY_V_WIND_COMPONENT"),
    ((0.925, 43.385, 87343.2), "QTY_VERTICAL_VELOCITY"),
    ((358.991, 45.981, 57959.7), "QTY_U_WIND_COMPONENT"),
    ((1.364, 45.333, 68452.7), "QTY_VERTICAL_VELOCITY"),
    ((358.178, 44.807, 98050.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((1.589, 43.985, 72274.6), "QTY_U10_WIND_COMPONENT"),
    ((359.004, 44.304, 60519.5), "QTY_VAPOR_MIXING_RATIO"),
    ((0.773, 44.140, 72794.2), "QTY_VERTICAL_VELOCITY"),
    ((359.366, 45.315, 86698.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.926, 44.487, 56146.2), "QTY_POTENTIAL_TEMPERATURE"),
    ((2.217, 44.877, 67330.1), "QTY_PRESSURE"),
    ((1.605, 45.499, 88432.0), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((359.970, 44.406, 74188.1), "QTY_VAPOR_MIXING_RATIO"),
    ((1.344, 44.848, 86916.1), "QTY_U10_WIND_COMPONENT"),
    ((357.963, 43.531, 90974.5), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.799, 44.203, 59846.0), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((1.200, 44.520, 55590.6), "QTY_V_WIND_COMPONENT"),
    ((0.126, 44.144, 91258.3), "QTY_RADAR_REFLECTIVITY"),
    ((1.690, 43.341, 53122.4), "QTY_CONDENSATIONAL_HEATING"),
    ((358.872, 43.202, 61554.1), "QTY_CONDENSATIONAL_HEATING"),
    ((359.708, 44.570, 56535.8), "QTY_PRESSURE"),
    ((2.206, 43.835, 91748.6), "QTY_U10_WIND_COMPONENT"),
    ((1.576, 44.375, 83397.8), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.285, 44.629, 77626.6), "QTY_VERTICAL_VELOCITY"),
    ((2.394, 45.757, 60650.2), "QTY_V_WIND_COMPONENT"),
    ((2.224, 45.415, 77293.9), "QTY_VAPOR_MIXING_RATIO"),
    ((1.535, 44.396, 62904.4), "QTY_2M_TEMPERATURE"),
    ((359.560, 43.311, 78356.1), "QTY_RAIN_NUMBER_CONCENTR"),
    ((359.650, 43.785, 89248.1), "QTY_VERTICAL_VELOCITY"),
    ((0.814, 43.901, 81052.8), "QTY_U10_WIND_COMPONENT"),
    ((358.621, 43.559, 97000.5), "QTY_U10_WIND_COMPONENT"),
    ((0.950, 44.913, 75505.7), "QTY_U10_WIND_COMPONENT"),
    ((1.431, 45.636, 52064.0), "QTY_PRESSURE"),
    ((358.838, 45.983, 80874.9), "QTY_SURFACE_PRESSURE"),
    ((359.496, 45.908, 82606.3), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((358.137, 46.408, 66569.3), "QTY_VAPOR_MIXING_RATIO"),
    ((0.131, 43.858, 79660.4), "QTY_CONDENSATIONAL_HEATING"),
    ((0.583, 43.975, 94477.0), "QTY_V10_WIND_COMPONENT"),
    ((359.980, 43.418, 52913.1), "QTY_V_WIND_COMPONENT"),
    ((358.336, 45.133, 73728.4), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((2.196, 44.227, 71868.1), "QTY_2M_TEMPERATURE"),
    ((357.833, 43.319, 64942.6), "QTY_SKIN_TEMPERATURE"),
    ((358.746, 44.088, 62744.8), "QTY_U10_WIND_COMPONENT"),
    ((359.909, 43.892, 70201.6), "QTY_LANDMASK"),
    ((0.770, 43.994, 62404.6), "QTY_RADAR_REFLECTIVITY"),
    ((0.151, 46.609, 58611.9), "QTY_2M_TEMPERATURE"),
    ((1.852, 46.422, 54750.3), "QTY_U_WIND_COMPONENT"),
    ((358.115, 45.794, 66091.6), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((359.204, 43.494, 61469.0), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((0.136, 43.589, 56107.1), "QTY_PRESSURE"),
    ((359.567, 43.239, 89505.1), "QTY_V_WIND_COMPONENT"),
    ((358.569, 43.926, 64797.4), "QTY_V_WIND_COMPONENT"),
    ((359.007, 44.809, 58954.2), "QTY_SKIN_TEMPERATURE"),
    ((0.491, 44.583, 56255.1), "QTY_U_WIND_COMPONENT"),
    ((0.788, 44.621, 90695.8), "QTY_CONDENSATIONAL_HEATING"),
    ((0.734, 46.624, 61372.4), "QTY_V10_WIND_COMPONENT"),
    ((359.379, 43.530, 61006.7), "QTY_RAIN_NUMBER_CONCENTR"),
    ((0.760, 44.766, 71768.0), "QTY_CONDENSATIONAL_HEATING"),
    ((2.203, 44.574, 92597.3), "QTY_LANDMASK"),
    ((1.000, 46.210, 52854.9), "QTY_SKIN_TEMPERATURE"),
    ((1.517, 43.198, 82911.2), "QTY_U_WIND_COMPONENT"),
    ((357.655, 44.118, 94960.2), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.393, 45.741, 88246.4), "QTY_CONDENSATIONAL_HEATING"),
    ((1.570, 45.032, 58996.9), "QTY_PRESSURE"),
    ((359.345, 44.331, 62220.1), "QTY_LANDMASK"),
    ((358.893, 44.969, 95176.4), "QTY_LANDMASK"),
    ((357.733, 43.278, 70092.3), "QTY_PRESSURE"),
    ((0.717, 43.613, 50396.1), "QTY_SURFACE_ELEVATION"),
    ((0.215, 44.404, 58323.7), "QTY_U_WIND_COMPONENT"),
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