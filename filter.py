# filter.py
'''
created by: Alka Tiwari
date: May 13, 2025
last updated: June 11, 2025
This Python script processes GeoTIFF (.tif) raster files in a given input directory by 
applying a pixel value threshold filter (15 cm) and writing the results to a new output directory.
It is designed for batch processing of flood depth rasters from FATHOM, 
where filtering low values (e.g., noise) is needed.

Input Arguments:
input_folder: Path to the directory containing .tif files.
output_root: Path to where the filtered output directory will be created.

Processing Steps:
Finds all .tif files in the input folder.
For each file:
    Reads the raster data and metadata.
    Sets pixel values below a defined threshold (15 cm) to a NoData value (-9999 if not already defined).
    Updates metadata with the new NoData value.
    Writes the filtered raster to an output directory named Filtered_<basename of input folder>.
    Skips processing if no .tif files are found in the input.

Logging:
A log file named filter_log.txt is created in the output_root.
It records:
    Start and end time for each folder processed.
    File-level statistics: minimum and maximum values of valid pixels after filtering.

Use filter_array.sh to run this on multiple folders on scratch preferably
'''
import os
import sys
import rasterio
import glob
from datetime import datetime

def log_message(log_path, message):
    with open(log_path, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")

def filter_and_save_tif(input_dir, output_root, threshold=15):
    tif_files = glob.glob(os.path.join(input_dir, "*.tif"))
    if not tif_files:
        print(f"No .tif files found in {input_dir}")
        return

    base_name = os.path.basename(input_dir.rstrip("/"))
    output_dir = os.path.join(output_root, f"Filtered_{base_name}")
    os.makedirs(output_dir, exist_ok=True)

    log_path = os.path.join(output_root, "filter_log.txt")
    log_message(log_path, f"Started processing folder: {input_dir}")
    count = 0

    for file in tif_files:
        with rasterio.open(file) as dataset:
            img = dataset.read(1)
            meta = dataset.meta

            nodata_value = dataset.nodata
            if nodata_value is None:
                nodata_value = -9999

            img[img < threshold] = nodata_value
            meta.update(nodata=nodata_value)

            output_path = os.path.join(output_dir, os.path.basename(file))
            with rasterio.open(output_path, 'w', **meta) as dst:
                dst.write(img, 1)

            # Log stats
            valid_pixels = img[img != nodata_value]
            min_val = valid_pixels.min() if valid_pixels.size > 0 else 'None'
            max_val = valid_pixels.max() if valid_pixels.size > 0 else 'None'
            log_message(log_path, f"  Processed {file} → min: {min_val}, max: {max_val}")
            count += 1

    log_message(log_path, f"Completed {count} files for {input_dir} → {output_dir}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python filter_tif.py <input_folder> <output_root>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_root = sys.argv[2]
    filter_and_save_tif(input_folder, output_root)

