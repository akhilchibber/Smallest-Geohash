# '''
# THE GOAL OF THIS PYTHON SCRIPT IS TO FIND THE SMALLEST POSSIBLE SINGLE GEOHASH FOR ANY GIVEN
# GEOSPATIAL DATASET IN .shp, .geojson, .tif, .png, and .jpeg FORMAT
# '''
#
#
#
#
#
# # IMPORTING THE ESSENTIAL LIBRARIES
# import os
# import fiona
# import rasterio
# import pygeohash as gh
# from PIL import Image
# from PIL.ExifTags import TAGS, GPSTAGS
#
#
#
#
#
# # FUNCTION 1: TO GET FILE EXTENSION
# def get_file_extension(file):
#     return os.path.splitext(file)[1]
#
#
#
#
#
# # FUNCTION 2: TO READ A GEOTIFF FILE
# def open_tiff_file(tiff_file):
#     return rasterio.open(tiff_file)
#
#
#
#
#
# # FUNCTION 3: TO GET BOUNDS OF A GEOTIFF FILE
# def load_tiff_bounds(tiff_file):
#     with open_tiff_file(tiff_file) as src:
#         bounds = src.bounds
#     return bounds
#
#
#
#
#
# # FUNCTION 4: TO READ A SHAPEFILE OR GEOJSON FILE
# def open_vector_file(vector_file):
#     return fiona.open(vector_file, 'r')
#
#
#
#
#
# # FUNCTION 5: TO GET BOUNDS OF A SHAPEFILE OR GEOJSON FILE
# def load_vector_bounds(vector_file):
#     with open_vector_file(vector_file) as src:
#         bounds = src.bounds
#     return bounds
#
#
#
#
#
# # FUNCTION 6: TO EXTRACT LATITUDE AND LONGITUDE FROM AN IMAGE
# def get_image_bounds(image_file):
#     img = Image.open(image_file)
#     try:
#         geotags = get_geotagging(img)
#         lat, lon = get_coordinates(geotags)
#         return (lon, lat, lon, lat)
#     except ValueError:
#         return None  # return None if no geolocation information is found
#
#
#
#
#
# # FUNCTION 7: TO GET GEOTAGGING
# def get_geotagging(img):
#     exif = img._getexif()
#     if not exif:
#         raise ValueError("No EXIF metadata found")
#
#     geotagging = {}
#     for (idx, tag) in TAGS.items():
#         if tag == 'GPSInfo':
#             if idx not in exif:
#                 raise ValueError("No EXIF geotagging found")
#
#             for (t, value) in GPSTAGS.items():
#                 if t in exif[idx]:
#                     geotagging[value] = exif[idx][t]
#
#     return geotagging
#
#
#
#
#
# # FUNCTION 8: TO GET DECIMAL FROM DMS
# def get_decimal_from_dms(dms, ref):
#     degrees = dms[0]
#     minutes = dms[1] / 60.0
#     seconds = dms[2] / 3600.0
#
#     if ref in ['S', 'W']:
#         degrees = -degrees
#         minutes = -minutes
#         seconds = -seconds
#
#     return round(degrees + minutes + seconds, 5)
#
#
#
#
#
# # FUNCTION 9: TO GET COORDINATES
# def get_coordinates(geotags):
#     lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
#     lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
#     return (lat,lon)
#
#
#
#
#
# # FUNCTION 10: TO IDENTIFY THE EXTREMES FOR MULTIPLE FILES
# def load_and_calculate_union_bounds(files):
#     minx, miny, maxx, maxy = [], [], [], []
#     for file in files:
#         extension = get_file_extension(file)
#         if extension in ['.shp', '.geojson']:
#             bounds = load_vector_bounds(file)
#         elif extension == '.tif':
#             bounds = load_tiff_bounds(file)
#         elif extension in ['.png', '.jpeg', '.jpg']:
#             bounds = get_image_bounds(file)
#             if bounds is None:
#                 print(f"No geolocation data found in {file}")
#                 return os.path.splitext(file)[0]  # return the image file name without extension if no geolocation information is found
#         else:
#             raise ValueError("Invalid file type. The file must be a Shapefile (.shp), GeoJSON (.geojson), GeoTiff (.tif), png (.png), or jpeg (.jpeg).")
#         minx.append(bounds[0])
#         miny.append(bounds[1])
#         maxx.append(bounds[2])
#         maxy.append(bounds[3])
#
#     union_bounds = (min(minx), min(miny), max(maxx), max(maxy))
#     return union_bounds
#
#
#
#
#
# # FUNCTION 7: Calculate Initial Geohash
# def calculate_initial_geohash(bounds, precision):
#     center_lng = (bounds[0] + bounds[2]) / 2  # calculate center longitude
#     center_lat = (bounds[1] + bounds[3]) / 2  # calculate center latitude
#     geohash = gh.encode(center_lat, center_lng, precision = precision)  # calculate geohash of center point with initial precision
#     return geohash
#
#
#
#
#
# # FUNCTION 8: Test Coverage
# def check_coverage(geohash, bounds):
#     lat_centroid, lon_centroid, lat_err, lon_err = gh.decode_exactly(geohash)  # decode geohash to its bounding box
#     gh_bounds = {
#         's': lat_centroid - lat_err,
#         'w': lon_centroid - lon_err,
#         'n': lat_centroid + lat_err,
#         'e': lon_centroid + lon_err
#     }
#     covers_area = gh_bounds['s'] <= bounds[1] and gh_bounds['w'] <= bounds[0] and gh_bounds['n'] >= bounds[3] and gh_bounds['e'] >= bounds[2]
#     # print(f"Does geohash {geohash} cover the entire area? {'Yes' if covers_area else 'No'}")
#     return covers_area
#
#
#
#
#
# # FUNCTION 9: Function to identify a list of smallest possible geohash which covers a given study area
# # This function is useful when we are not able to bound a study area in 1 geohash
# def generate_geohashes(bounds):
#     lat_step = (bounds[3] - bounds[1]) / 5.0
#     lon_step = (bounds[2] - bounds[0]) / 5.0
#     geohashes = set()  # change this to a set to ensure uniqueness
#
#     for lat in range(0, 5):
#         for lon in range(0, 5):
#             min_lat = bounds[1] + lat * lat_step
#             max_lat = min_lat + lat_step
#             min_lon = bounds[0] + lon * lon_step
#             max_lon = min_lon + lon_step
#             center_lat = (min_lat + max_lat) / 2.0
#             center_lon = (min_lon + max_lon) / 2.0
#             geohash = gh.encode(center_lat, center_lon, precision = 1)
#             geohashes.add(geohash)  # add the geohash to the set
#
#     return list(geohashes)  # convert back to a list for the return
#
#
#
#
#
# # FUNCTION 10: Identify the Extremes, Precision Adjustment and Iterative Refinement
# # FUNCTION TO IDENTIFY THE SMALLEST POSSIBLE GEOHASH WHICH COVERS A GIVEN STUDY AREA
# def find_smallest_geohash(dataset, initial_precision=10):
#     # It now accepts a list of dataset instead of just one
#     if isinstance(dataset, str):
#         dataset = [dataset]  # if a single file is provided, turn it into a list
#
#     bounds = load_and_calculate_union_bounds(dataset)
#
#     if isinstance(bounds, str):  # if bounds is a string, it's the file name
#         return bounds
#
#     geohash = calculate_initial_geohash(bounds, initial_precision)  # Step 2: Calculate initial geohash
#     covers_area = check_coverage(geohash, bounds)  # Step 3: Test coverage
#
#     # if the geohash bounding box doesn't cover the entire city, decrement precision
#     while not covers_area and initial_precision > 1:  # Step 4: Precision adjustment
#         initial_precision -= 1  # Step 5: Iterative refinement
#         geohash = calculate_initial_geohash(bounds, initial_precision)
#         covers_area = check_coverage(geohash, bounds)
#
#     # Ensure the final geohash covers the entire area
#     if covers_area:
#         smallest_geohash = geohash
#     else:
#         geohashes = generate_geohashes(bounds)  # Here we generate all geohashes for the area
#         # If there's only one geohash, return it as a string, not a list
#         smallest_geohash = geohashes[0] if len(geohashes) == 1 else geohashes
#
#     return smallest_geohash
#
#
#
#
#
# # End of the Python Script
'''
THE GOAL OF THIS PYTHON SCRIPT IS TO FIND THE SMALLEST POSSIBLE SINGLE GEOHASH FOR ANY GIVEN
GEOSPATIAL DATASET IN .shp, .geojson, .tif, .png, and .jpeg FORMAT
'''

# Importing the essential Libraries
import os
import fiona
import rasterio
import pygeohash as gh
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# FUNCTION 1: TO GET FILE EXTENSION
def get_file_extension(file):
    return os.path.splitext(file)[1]

# FUNCTION 2: TO READ A GEOTIFF FILE
def open_tiff_file(tiff_file):
    return rasterio.open(tiff_file)

# FUNCTION 3: TO GET BOUNDS OF A GEOTIFF FILE
def load_tiff_bounds(tiff_file):
    with open_tiff_file(tiff_file) as src:
        bounds = src.bounds
    return bounds

# FUNCTION 4: TO READ A SHAPEFILE OR GEOJSON FILE
def open_vector_file(vector_file):
    return fiona.open(vector_file, 'r')

# FUNCTION 5: TO GET BOUNDS OF A SHAPEFILE OR GEOJSON FILE
def load_vector_bounds(vector_file):
    with open_vector_file(vector_file) as src:
        bounds = src.bounds
    return bounds

# FUNCTION 6: TO EXTRACT LATITUDE AND LONGITUDE FROM AN IMAGE
def get_image_bounds(image_file):
    img = Image.open(image_file)
    try:
        geotags = get_geotagging(img)
        lat, lon = get_coordinates(geotags)
        return (lon, lat, lon, lat)
    except ValueError:
        return image_file  # return the image file name if no geolocation information is found

# FUNCTION 7: TO GET GEOTAGGING
def get_geotagging(img):
    exif = img._getexif()
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (t, value) in GPSTAGS.items():
                if t in exif[idx]:
                    geotagging[value] = exif[idx][t]

    return geotagging

# FUNCTION 8: TO GET DECIMAL FROM DMS
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

# FUNCTION 9: TO GET COORDINATES
def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)

# FUNCTION 10: TO IDENTIFY THE EXTREMES FOR MULTIPLE FILES
# FUNCTION 10: TO IDENTIFY THE EXTREMES FOR MULTIPLE FILES
def load_and_calculate_union_bounds(files):
    minx, miny, maxx, maxy = [], [], [], []
    no_geolocation_data = False
    for file in files:
        extension = get_file_extension(file)
        if extension in ['.shp', '.geojson']:
            bounds = load_vector_bounds(file)
        elif extension == '.tif':
            bounds = load_tiff_bounds(file)
        elif extension in ['.png', '.jpeg', '.jpg']:
            bounds = get_image_bounds(file)
            if isinstance(bounds, str):  # No geolocation data found
                print(f"No geolocation data found in {file}")
                no_geolocation_data = True
                continue
        else:
            raise ValueError("Invalid file type. The file must be a Shapefile (.shp), GeoJSON (.geojson), GeoTiff (.tif), png (.png), or jpeg (.jpeg).")
        minx.append(bounds[0])
        miny.append(bounds[1])
        maxx.append(bounds[2])
        maxy.append(bounds[3])

    if no_geolocation_data and not (minx and miny and maxx and maxy):  # No bounds were added
        return 'No geolocation data'

    union_bounds = (min(minx), min(miny), max(maxx), max(maxy))
    return union_bounds





# FUNCTION 7: Calculate Initial Geohash
def calculate_initial_geohash(bounds, precision):
    center_lng = (bounds[0] + bounds[2]) / 2  # calculate center longitude
    center_lat = (bounds[1] + bounds[3]) / 2  # calculate center latitude
    geohash = gh.encode(center_lat, center_lng, precision = precision)  # calculate geohash of center point with initial precision
    return geohash





# FUNCTION 8: Test Coverage
def check_coverage(geohash, bounds):
    lat_centroid, lon_centroid, lat_err, lon_err = gh.decode_exactly(geohash)  # decode geohash to its bounding box
    gh_bounds = {
        's': lat_centroid - lat_err,
        'w': lon_centroid - lon_err,
        'n': lat_centroid + lat_err,
        'e': lon_centroid + lon_err
    }
    covers_area = gh_bounds['s'] <= bounds[1] and gh_bounds['w'] <= bounds[0] and gh_bounds['n'] >= bounds[3] and gh_bounds['e'] >= bounds[2]
    # print(f"Does geohash {geohash} cover the entire area? {'Yes' if covers_area else 'No'}")
    return covers_area





# FUNCTION 9: Function to identify a list of smallest possible geohash which covers a given study area
# This function is useful when we are not able to bound a study area in 1 geohash
def generate_geohashes(bounds):
    lat_step = (bounds[3] - bounds[1]) / 5.0
    lon_step = (bounds[2] - bounds[0]) / 5.0
    geohashes = set()  # change this to a set to ensure uniqueness

    for lat in range(0, 5):
        for lon in range(0, 5):
            min_lat = bounds[1] + lat * lat_step
            max_lat = min_lat + lat_step
            min_lon = bounds[0] + lon * lon_step
            max_lon = min_lon + lon_step
            center_lat = (min_lat + max_lat) / 2.0
            center_lon = (min_lon + max_lon) / 2.0
            geohash = gh.encode(center_lat, center_lon, precision = 1)
            geohashes.add(geohash)  # add the geohash to the set

    return list(geohashes)  # convert back to a list for the return





# FUNCTION 10: Identify the Extremes, Precision Adjustment and Iterative Refinement
# FUNCTION TO IDENTIFY THE SMALLEST POSSIBLE GEOHASH WHICH COVERS A GIVEN STUDY AREA
def find_smallest_geohash(dataset, initial_precision = 10):
    # it now accepts a list of dataset instead of just one
    if isinstance(dataset, str):
        dataset = [dataset]  # if a single file is provided, turn it into a list

    bounds = load_and_calculate_union_bounds(dataset)

    if bounds == 'No geolocation data':  # No geolocation data found in any JPG/PNG file
        return '7zzzzzzzzz'

    geohash = calculate_initial_geohash(bounds, initial_precision)  # Step 2: Calculate initial geohash
    covers_area = check_coverage(geohash, bounds)  # Step 3: Test coverage

    # if the geohash bounding box doesn't cover the entire city, decrement precision
    while not covers_area and initial_precision > 1:  # Step 4: Precision adjustment
        initial_precision -= 1  # Step 5: Iterative refinement
        geohash = calculate_initial_geohash(bounds, initial_precision)
        covers_area = check_coverage(geohash, bounds)

    # Ensure the final geohash covers the entire area
    if covers_area:
        smallest_geohash = geohash
    else:
        geohashes = generate_geohashes(bounds)  # Here we generate all geohashes for the area
        # If there's only one geohash, return it as a string, not a list
        smallest_geohash = geohashes[0] if len(geohashes) == 1 else geohashes

    return smallest_geohash





# End of the Python Script