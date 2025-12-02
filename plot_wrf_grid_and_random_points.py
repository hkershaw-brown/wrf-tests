import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from shapely.geometry import Point, Polygon

# Read XLON and XLAT from netCDF file
nc_file = 'wrfinput_d01'
with Dataset(nc_file, 'r') as nc:
    xlon = nc.variables['XLONG'][0]
    xlat = nc.variables['XLAT'][0]

# Plot the points on a map
plt.figure(figsize=(8, 6))
plt.scatter(xlon, xlat, s=1, c='blue', label='Grid Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('WRF Grid Points')
plt.legend()
plt.grid(True)
plt.show()

# Get the boundary polygon
lon_flat = xlon.flatten()
lat_flat = xlat.flatten()
points = np.column_stack((lon_flat, lat_flat))
polygon = Polygon(points)

# Generate N=100 random points within the bounding box
N = 100
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

# Plot random points
plt.figure(figsize=(8, 6))
plt.scatter(xlon, xlat, s=1, c='blue', label='Grid Points')
plt.scatter(random_points[:, 0], random_points[:, 1], c='red', s=10, label='Random Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('WRF Grid and Random Points')
plt.legend()
plt.grid(True)
plt.show()

# Format random points for test_interp.py
#     "QTY_SURFACE_PRESSURE" needs vertissurface
quantities = [
    "QTY_POTENTIAL_TEMPERATURE",
    "QTY_U_WIND_COMPONENT",
    "QTY_V_WIND_COMPONENT",
    "QTY_PRESSURE",
    "QTY_GEOPOTENTIAL_HEIGHT",
    "QTY_VERTICAL_VELOCITY",
    "QTY_VAPOR_MIXING_RATIO",
    "QTY_U10_WIND_COMPONENT",
    "QTY_V10_WIND_COMPONENT",
    "QTY_SURFACE_PRESSURE",
    "QTY_2M_TEMPERATURE",
    "QTY_SKIN_TEMPERATURE",
    "QTY_LANDMASK",
    "QTY_SURFACE_ELEVATION",
    "QTY_RADAR_REFLECTIVITY",
    "QTY_CONDENSATIONAL_HEATING",
    "QTY_RAIN_NUMBER_CONCENTR",
    "QTY_CLOUDWATER_MIXING_RATIO"
]

# not in wrf file:
# "QTY_2M_SPECIFIC_HUMIDITY"

heights = np.random.uniform(400, 2000, N)
pressures = np.random.uniform(50000, 100000, N)  # Example pressures in Pa
levels = np.random.randint(1, 30, N)  # Example model levels
scaleheights = np.random.uniform(7000, 9000, N)  # Example scale heights in meters
test_cases = []
for i in range(N):
    lon, lat = random_points[i]
    # Convert longitude to 0-360
    lon_360 = lon if lon >= 0 else lon + 360
    lon_360 = lon_360 % 360
    height = round(heights[i], 1)
    pressure = round(pressures[i], 1)
    level = levels[i]
    #scaleheight = round(scaleheights[i], 1)
    qty = np.random.choice(quantities)
    #test_cases.append(f"(({lon_360:.3f}, {lat:.3f}, {height}), \"{qty}\")")
    test_cases.append(f"(({lon_360:.3f}, {lat:.3f}, {pressure}), \"{qty}\")")
    #test_cases.append(f"(({lon_360:.3f}, {lat:.3f}, {level}), \"{qty}\")")
    #test_cases.append(f"(({lon_360:.3f}, {lat:.3f}, {scaleheight}), \"{qty}\")")


print("test_cases = [")
for case in test_cases:
    print(f"    {case},")
print("]")
