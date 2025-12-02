import subprocess
import shutil
import os
import re
import pytest

# currently hand setting vertiscal coordinate to use in input.X.nml
NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "input.old.nml"
#NML_PATH_2 = "input.new.nml"
verticoord = "VERTISPRESSURE"  # options: VERTISHEIGHT, VERTISPRESSURE, VERTISSURFACE, VERTISLEVEL, VERTISUNDEF

WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"
EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf/work/model_mod_check"
#EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"

test_cases = [
    ((357.803, 44.189, 68857.2), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((358.350, 44.052, 94845.6), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.491, 43.698, 50104.3), "QTY_CONDENSATIONAL_HEATING"),
    ((1.194, 45.149, 61093.8), "QTY_SURFACE_ELEVATION"),
    ((359.029, 45.005, 55124.9), "QTY_RADAR_REFLECTIVITY"),
    ((0.722, 44.572, 87874.8), "QTY_CONDENSATIONAL_HEATING"),
    ((0.224, 44.028, 95716.1), "QTY_SURFACE_PRESSURE"),
    ((0.081, 44.283, 66971.6), "QTY_2M_TEMPERATURE"),
    ((1.188, 44.343, 89824.4), "QTY_RAIN_NUMBER_CONCENTR"),
    ((358.294, 44.291, 68068.6), "QTY_SURFACE_PRESSURE"),
    ((358.883, 44.289, 92114.1), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.594, 44.265, 71354.8), "QTY_SURFACE_PRESSURE"),
    ((0.254, 46.464, 90473.3), "QTY_2M_TEMPERATURE"),
    ((359.617, 43.205, 67538.7), "QTY_SURFACE_ELEVATION"),
    ((0.705, 44.067, 83118.8), "QTY_SURFACE_PRESSURE"),
    ((359.552, 43.937, 95009.5), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((0.588, 44.887, 59930.9), "QTY_U_WIND_COMPONENT"),
    ((357.627, 46.548, 72306.3), "QTY_RAIN_NUMBER_CONCENTR"),
    ((357.925, 44.408, 99890.5), "QTY_2M_TEMPERATURE"),
    ((359.729, 43.236, 78588.6), "QTY_LANDMASK"),
    ((358.356, 45.539, 66234.1), "QTY_PRESSURE"),
    ((1.528, 44.087, 76003.9), "QTY_VAPOR_MIXING_RATIO"),
    ((358.909, 43.613, 63417.9), "QTY_U_WIND_COMPONENT"),
    ((1.240, 44.335, 97387.7), "QTY_U_WIND_COMPONENT"),
    ((358.083, 44.649, 57859.0), "QTY_SURFACE_ELEVATION"),
    ((357.892, 45.601, 56341.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.450, 43.684, 90222.3), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((1.197, 44.124, 77696.6), "QTY_LANDMASK"),
    ((0.918, 44.302, 72893.2), "QTY_2M_TEMPERATURE"),
    ((1.815, 43.280, 92341.2), "QTY_PRESSURE"),
    ((358.983, 46.377, 54890.1), "QTY_SURFACE_ELEVATION"),
    ((1.579, 43.421, 60388.8), "QTY_SKIN_TEMPERATURE"),
    ((358.553, 44.126, 61969.2), "QTY_V10_WIND_COMPONENT"),
    ((1.979, 43.858, 51364.3), "QTY_VAPOR_MIXING_RATIO"),
    ((359.073, 43.825, 76628.2), "QTY_CONDENSATIONAL_HEATING"),
    ((359.428, 44.685, 66308.6), "QTY_PRESSURE"),
    ((1.591, 43.817, 70070.3), "QTY_V10_WIND_COMPONENT"),
    ((359.685, 44.677, 77647.9), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((2.088, 43.690, 61820.6), "QTY_POTENTIAL_TEMPERATURE"),
    ((0.170, 43.832, 98435.1), "QTY_U_WIND_COMPONENT"),
    ((1.378, 46.767, 90196.6), "QTY_V_WIND_COMPONENT"),
    ((359.972, 44.530, 91791.0), "QTY_U10_WIND_COMPONENT"),
    ((357.558, 46.585, 67055.9), "QTY_VERTICAL_VELOCITY"),
    ((358.471, 44.318, 67093.6), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((359.244, 43.610, 63701.3), "QTY_RADAR_REFLECTIVITY"),
    ((1.063, 44.990, 81834.9), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.495, 43.909, 98532.6), "QTY_SKIN_TEMPERATURE"),
    ((0.464, 44.651, 55683.1), "QTY_V_WIND_COMPONENT"),
    ((0.098, 44.724, 57222.1), "QTY_V10_WIND_COMPONENT"),
    ((1.759, 45.149, 56224.9), "QTY_SURFACE_PRESSURE"),
    ((1.680, 43.806, 54656.2), "QTY_U10_WIND_COMPONENT"),
    ((357.996, 46.318, 76586.6), "QTY_SURFACE_ELEVATION"),
    ((0.226, 43.877, 59501.6), "QTY_SKIN_TEMPERATURE"),
    ((359.804, 44.621, 55089.7), "QTY_U10_WIND_COMPONENT"),
    ((0.660, 44.963, 72934.1), "QTY_VERTICAL_VELOCITY"),
    ((1.622, 44.636, 57898.5), "QTY_LANDMASK"),
    ((358.429, 45.695, 73313.9), "QTY_LANDMASK"),
    ((1.884, 44.036, 92320.0), "QTY_SKIN_TEMPERATURE"),
    ((1.949, 44.253, 96668.5), "QTY_SURFACE_ELEVATION"),
    ((1.407, 44.945, 69718.1), "QTY_V10_WIND_COMPONENT"),
    ((1.541, 44.002, 89492.1), "QTY_SURFACE_ELEVATION"),
    ((1.244, 45.058, 93389.9), "QTY_V_WIND_COMPONENT"),
    ((0.342, 44.075, 86370.0), "QTY_V10_WIND_COMPONENT"),
    ((357.916, 43.742, 91657.0), "QTY_VERTICAL_VELOCITY"),
    ((357.936, 43.922, 99826.3), "QTY_2M_TEMPERATURE"),
    ((359.739, 44.545, 54399.6), "QTY_U_WIND_COMPONENT"),
    ((358.891, 45.406, 65030.6), "QTY_LANDMASK"),
    ((0.362, 44.687, 72053.4), "QTY_SKIN_TEMPERATURE"),
    ((359.911, 43.757, 56942.3), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.215, 45.186, 50652.6), "QTY_SKIN_TEMPERATURE"),
    ((359.974, 43.738, 52206.6), "QTY_U_WIND_COMPONENT"),
    ((357.655, 44.552, 56167.5), "QTY_SKIN_TEMPERATURE"),
    ((1.503, 45.168, 86560.5), "QTY_PRESSURE"),
    ((1.219, 43.752, 70081.7), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.840, 43.267, 61591.9), "QTY_SURFACE_ELEVATION"),
    ((0.493, 45.128, 76539.8), "QTY_VERTICAL_VELOCITY"),
    ((359.450, 43.982, 87242.8), "QTY_SURFACE_ELEVATION"),
    ((1.756, 43.349, 84493.3), "QTY_SURFACE_ELEVATION"),
    ((357.772, 46.532, 88290.7), "QTY_LANDMASK"),
    ((1.369, 44.375, 72285.1), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((1.013, 44.317, 57597.7), "QTY_VERTICAL_VELOCITY"),
    ((357.990, 44.229, 78790.3), "QTY_SKIN_TEMPERATURE"),
    ((359.679, 43.252, 56249.6), "QTY_RAIN_NUMBER_CONCENTR"),
    ((359.417, 44.298, 61714.3), "QTY_VAPOR_MIXING_RATIO"),
    ((357.915, 46.497, 53646.9), "QTY_RADAR_REFLECTIVITY"),
    ((359.824, 43.419, 95657.6), "QTY_U10_WIND_COMPONENT"),
    ((1.468, 44.258, 75080.2), "QTY_V10_WIND_COMPONENT"),
    ((0.933, 44.920, 91002.2), "QTY_SURFACE_PRESSURE"),
    ((1.129, 45.027, 53180.4), "QTY_V10_WIND_COMPONENT"),
    ((358.238, 45.063, 86494.3), "QTY_CLOUDWATER_MIXING_RATIO"),
    ((358.207, 45.964, 85409.9), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((1.504, 46.692, 72222.1), "QTY_SURFACE_ELEVATION"),
    ((359.617, 44.077, 59583.7), "QTY_SKIN_TEMPERATURE"),
    ((358.309, 44.703, 91035.0), "QTY_V_WIND_COMPONENT"),
    ((1.635, 44.393, 98830.3), "QTY_POTENTIAL_TEMPERATURE"),
    ((1.232, 43.307, 83035.3), "QTY_VERTICAL_VELOCITY"),
    ((1.498, 45.358, 77507.6), "QTY_GEOPOTENTIAL_HEIGHT"),
    ((359.780, 43.691, 58248.6), "QTY_POTENTIAL_TEMPERATURE"),
    ((358.598, 44.373, 56161.7), "QTY_2M_TEMPERATURE"),
    ((359.189, 43.599, 53991.9), "QTY_LANDMASK"),
]

def update_nml(nml_path, loc, qty, vertcoord):
    with open(nml_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if "loc_of_interest" in line:
            new_lines.append(f"   loc_of_interest       = {loc[0]}, {loc[1]}, {loc[2]}\n")
        elif "quantity_of_interest" in line:
            new_lines.append(f"   quantity_of_interest  = '{qty}'\n")
        elif "interp_test_vertcoord" in line:
            new_lines.append(f"interp_test_vertcoord = '{vertcoord}'\n")
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
    update_nml(WORK_NML_PATH, loc, qty, verticoord)
    result1 = run_model_mod_check(EXE_PATH_1)
    assert result1.returncode == 0, f"model_mod_check_v1 failed: {result1.stderr}"
    value1, type1 = extract_value(result1.stdout)

    # Run v2
    shutil.copyfile(NML_PATH_2, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty, verticoord)
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