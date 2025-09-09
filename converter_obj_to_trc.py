# -*- coding: utf-8 -*-

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% SMPL-Vertices to *.trc file converter %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Script to process data recorded with OpenCap and stored using the OpenCap 
folder structure. 

The script searches the specified root directory for all folders matching 
a user-defined folder (e.g., "CameraHMR"). Within each matching folder, 
it recursively looks for subfolders containing SMPL output files (*.obj). 

For each such subfolder, the script:
    - Extracts marker positions from a series of *.obj files using predefined vertex IDs.
    - Saves the results as a TRC file in a corresponding output folder named 
      "MarkerData_<user-defined folder>" (e.g., "MarkerData_CameraHMR"), located at the 
      same hierarchy level as the original search-tag folder.

User Settings:
- Vertices IDs: Dictionary mapping marker names to their corresponding vertex IDs.
- Frame rate: Set the frame rate for the data.
- Root folder: Set the root folder containing all subfolders of interest.

Author: Brian Horsak, brian.horsak@fhstp.ac.at
Date: 03/2025
"""

import os
import utils

# %% User Settings.

# Hardcoded vertices-IDs mapping marker names to their corresponding vertex IDs.
initial_marker_vertices = {
    "RASI": 6573, "LASI": 3156, "SACR": 3159,
    "RKNE": 4495, "RKNM": 4634, "RTT": 4664,
    "RANK": 6727, "RANM": 6833, "RHEE": 6786,
    "RTOE": 6741, "RD1M": 6750, "RD5M": 6715,
    "LKNE": 1010, "LKNM": 1148, "LTT": 1178,
    "LANK": 3327, "LANM": 3433, "LHEE": 3387,
    "LTOE": 3340, "LD1M": 3350, "LD5M": 3348,
    "T10": 3015, "C7": 828, "CLAV": 3078, "STRN": 3076,
    "LSHO": 1239, "LELB": 1658, "LUPA": 1505,
    "LWRA": 2112, "LWRB": 2108, "LFIN": 2135,
    "RSHO": 4724, "RELB": 5129, "RUPA": 6282,
    "RWRA": 5573, "RWRB": 5608, "RFIN": 5595
}

# Set frame rate with which the obj files were created.
frame_rate = 60  # Adjust as needed

# Set root folder containing all subfolders of interest.
root_folder = r".\data"

# Set the folder tag to search for (e.g., "CameraHMR", "OpenPose", "SomethingElse")
search_tag = "CameraHMR"

# %% Find and process all folders with the given search tag and their subdirectories with OBJ files.

# Find all folders that contain a subfolder named search_tag
tagged_folders = utils.find_marker_data_folders(root_folder, search_tag)

# Process each found folder.
for tagged_folder in tagged_folders:
    print(f"\nProcessing {search_tag} folder: {tagged_folder}")
    
    # Walk through all subdirectories of the tagged folder.
    for subdir, dirs, files in os.walk(tagged_folder):
        
        # Check if the subdirectory contains any .obj files.
        obj_files = [f for f in files if f.endswith('.obj')]
        
        if obj_files:
            print(f"  Found subfolder with OBJ files: {subdir}")
            try:
                # Extract marker data from this subfolder.
                marker_positions, output_filename = utils.extract_vertex_timeseries(
                    subdir, initial_marker_vertices
                )
                
                # Remove the last subfolder from the path.
                parent_dir = os.path.dirname(subdir)

                # Convert the path into parts and replace only the exact match of search_tag
                path_parts = parent_dir.split(os.sep)
                for i, part in enumerate(path_parts):
                    if part == search_tag:  # Exact match check
                        path_parts[i] = f"MarkerData_{search_tag}"
                        break  # Stop after the first replacement
                
                # Rebuild the path
                output_folder = os.sep.join(path_parts)

                utils.ensure_folder_exists(output_folder)
                output_file = os.path.join(output_folder, output_filename + '.trc')
                print(f">>> Saving TRC file to: {output_file}")
                utils.save_to_trc(initial_marker_vertices, marker_positions, frame_rate, output_file)
            
            except Exception as e:
                print(f">>> Error processing folder {subdir}: {e}")
