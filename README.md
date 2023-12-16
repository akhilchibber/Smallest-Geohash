# Finding the Smallest Geohash to Bound Geospatial Dataset
<p align="center">
  <img src="https://github.com/akhilchibber/Smallest-Geohash/blob/main/geohash.jpeg?raw=true" alt="earthml Logo">
</p>
Welcome to the Smallest GeoHash Finder repository! This Python script is designed to determine the smallest possible single GeoHash for any given geospatial dataset. It supports multiple file formats including `.shp`, `.geojson`, `.tif`, `.png`, and `.jpeg`.

## Overview

GeoHash is a compact encoding of geographic locations that simplifies spatial data representation. Our script aims to find the most precise and concise GeoHash representation for a given geospatial dataset, ensuring efficient storage and retrieval.

## How It Works

The script follows these key steps:

1. **File Handling:** Determines the file type and processes accordingly - Shapefiles, GeoJSON, GeoTIFF, and images with geotagging (PNG, JPEG).
2. **Bounding Box Calculation:** Extracts or calculates the bounding box for each file.
3. **GeoHash Calculation:** Computes an initial GeoHash based on the bounding box and refines it to the smallest possible GeoHash that still covers the entire dataset.
4. **GeoHash Generation:** If a single GeoHash cannot cover the entire area, the script generates multiple smaller GeoHashes.

### Supported Formats

- **Shapefile (.shp)**
- **GeoJSON (.geojson)**
- **GeoTIFF (.tif)**
- **Images (PNG, JPEG) with geolocation metadata**

## Getting Started

To use this script, ensure Python is installed on your system along with necessary libraries such as `os`, `fiona`, `rasterio`, `pygeohash`, and `PIL`.

### Prerequisites

- Python 3.x
- Libraries: `os`, `fiona`, `rasterio`, `pygeohash`, `PIL`

### Running the Script

1. Place your geospatial datasets in an accessible directory.
2. Run the script by passing the file paths to the function `find_smallest_geohash`.
3. The script will output the smallest possible GeoHash or a set of GeoHashes covering the dataset.

## Why Use This Script?

- **Versatility:** Works with various geospatial data formats.
- **Precision:** Finds the most accurate GeoHash covering the entire dataset.
- **Ease of Use:** Simplifies complex geospatial calculations into a straightforward process.

## Contributing

We welcome contributions to enhance the functionality and efficiency of this script. Feel free to fork, modify, and make pull requests to this repository. To contribute:

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request against the `main` branch.

## License

This project is licensed under the MIT License - see the `LICENSE` file for more details.

## Contact

Author - Akhil Chhibber

LinkedIn: https://www.linkedin.com/in/akhilchhibber/

Blog: https://medium.com/@akhil.chibber/finding-the-smallest-geohash-to-bound-geospatial-dataset-ece3a457b443
