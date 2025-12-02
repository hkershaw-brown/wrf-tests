import numpy as np
from netCDF4 import Dataset
from shapely.geometry import Point, Polygon
import subprocess
import shutil
import os
import re
import pytest

NML_PATH_1 = "input.new.nml"
NML_PATH_2 = "input.old.nml"
WORK_NML_PATH = "input.nml"
BACKUP_PATH = WORK_NML_PATH + ".bak"
EXE_PATH_1 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf_unified/work/model_mod_check"
EXE_PATH_2 = "/Users/hkershaw/DART/Projects/wrf_refactor/DART.wrf-wrf-chem/models/wrf/work/model_mod_check"

def generate_test_cases_for_vertcoord(vertcoord, N=100, nc_file='wrfinput_d01'):
    """
    Generate N test cases for the given vertical coordinate system using the WRF grid.
    vertcoord: str, one of VERTISHEIGHT, VERTISPRESSURE, VERTISSURFACE, VERTISLEVEL, VERTISUNDEF
    Returns a list of ((lon, lat, vert), quantity) tuples.
    """
    with Dataset(nc_file, 'r') as nc:
        xlon = nc.variables['XLONG'][0]
        xlat = nc.variables['XLAT'][0]
    lon_flat = xlon.flatten()
    lat_flat = xlat.flatten()
    points = np.column_stack((lon_flat, lat_flat))
    polygon = Polygon(points)
    min_lon, max_lon = lon_flat.min(), lon_flat.max()
    min_lat, max_lat = lat_flat.min(), lat_flat.max()
    random_points = []
    while len(random_points) < N:
        lon_rand = np.random.uniform(min_lon, max_lon)
        lat_rand = np.random.uniform(min_lat, max_lat)
        pt = Point(lon_rand, lat_rand)
        if polygon.contains(pt):
            random_points.append((lon_rand, lat_rand))
    random_points = np.array(random_points)

    # Quantities to choose from
    quantities = [
        "QTY_POTENTIAL_TEMPERATURE",
        "QTY_U_WIND_COMPONENT",
        "QTY_V_WIND_COMPONENT",
        "QTY_PRESSURE",
        "QTY_GEOPOTENTIAL_HEIGHT",
        "QTY_VERTICAL_VELOCITY",
        "QTY_VAPOR_MIXING_RATIO",
        "QTY_QVAPOR",
        "QTY_SURFACE_PRESSURE",
        "QTY_U10_WIND_COMPONENT",
        "QTY_V10_WIND_COMPONENT"
    ]

    #np.random.seed(42)  # For reproducibility
    heights = np.random.uniform(400, 2000, N)
    pressures = np.random.uniform(50000, 100000, N)
    levels = np.random.randint(1, 30, N)

    test_cases = []
    for i in range(N):
        lon, lat = random_points[i]
        lon_360 = lon if lon >= 0 else lon + 360
        lon_360 = lon_360 % 360
        qty = np.random.choice(quantities)
        if vertcoord == "VERTISHEIGHT":
            vert = round(heights[i], 1)
        elif vertcoord == "VERTISPRESSURE":
            vert = round(pressures[i], 1)
        elif vertcoord == "VERTISSURFACE":
            vert = 1
        elif vertcoord == "VERTISLEVEL":
            vert = int(levels[i])
        elif vertcoord == "VERTISUNDEF":
            vert = 0
        else:
            raise ValueError(f"Unknown vertcoord: {vertcoord}")
        test_cases.append(((round(lon_360, 3), round(lat, 3), vert), qty))
    return test_cases

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


# Generate all (verticoord, test_case) pairs for parametrization
#vertical_options = ["VERTISHEIGHT", "VERTISPRESSURE", "VERTISSURFACE", "VERTISLEVEL", "VERTISUNDEF"]
vertical_options = ["VERTISHEIGHT", "VERTISPRESSURE", "VERTISLEVEL"]

all_test_params = []
for verticoord in vertical_options:
    cases = generate_test_cases_for_vertcoord(verticoord)
    for test_case in cases:
        all_test_params.append((verticoord, test_case))

@pytest.mark.parametrize("verticoord,test_case", all_test_params)
def test_model_mod_check_equality(verticoord, test_case):
    loc, qty = test_case
    print(f"RUNNING: verticoord={verticoord}, test_case=(({loc[0]}, {loc[1]}, {loc[2]}), \"{qty}\")")
    shutil.copyfile(NML_PATH_1, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty, verticoord)
    result1 = run_model_mod_check(EXE_PATH_1)
    assert result1.returncode == 0, f"model_mod_check_v1 failed: {result1.stderr}"
    value1, type1 = extract_value(result1.stdout)

    shutil.copyfile(NML_PATH_2, WORK_NML_PATH)
    update_nml(WORK_NML_PATH, loc, qty, verticoord)
    result2 = run_model_mod_check(EXE_PATH_2)
    assert result2.returncode == 0, f"model_mod_check_v2 failed: {result2.stderr}"
    value2, type2 = extract_value(result2.stdout)

    print(f"Value from v1: {value1} ({type1}), Value from v2: {value2} ({type2})")
    if type1 == 'error' and type2 == 'error':
        assert True
    else:
        if not (value1 == value2 and type1 == type2):
            print(f"FAIL: verticoord={verticoord}, test_case=(({loc[0]}, {loc[1]}, {loc[2]}), \"{qty}\")")
        assert value1 == value2 and type1 == type2, f"Values/type differ: {value1} ({type1}) != {value2} ({type2})"