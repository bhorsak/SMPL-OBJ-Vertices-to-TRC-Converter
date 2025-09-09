# -*- coding: utf-8 -*-
import os
import numpy as np
#import json


def compute_transformation_matrix(vertex_data):
    """
    Compute the transformation matrix to align the floor plane with the X-Z plane and center the origin.
    """
    rhee, rtoe = np.array(vertex_data['RHEE'][0]), np.array(vertex_data['RTOE'][0])
    lhee, ltoe = np.array(vertex_data['LHEE'][0]), np.array(vertex_data['LTOE'][0])

    origin = (rhee + rtoe + lhee + ltoe) / 4  # Midpoint of markers
    x_axis = rtoe - rhee  # Heel to toe direction
    x_axis /= np.linalg.norm(x_axis) if np.linalg.norm(x_axis) != 0 else np.array([1, 0, 0])

    temp_y_axis = np.cross(x_axis, (ltoe - rtoe))
    temp_y_axis /= np.linalg.norm(temp_y_axis) if np.linalg.norm(temp_y_axis) != 0 else np.array([0, 1, 0])

    z_axis = np.cross(temp_y_axis, x_axis)  # Adjusted to ensure right-handed coordinate system
    z_axis /= np.linalg.norm(z_axis)

    y_axis = np.cross(z_axis, x_axis)  # Ensure perpendicularity

    # Ensure y-axis points up
    if y_axis[1] < 0:
        y_axis = -y_axis
        z_axis = -z_axis

    rotation_matrix = np.vstack([x_axis, y_axis, z_axis]).T
    translation_vector = -rotation_matrix @ origin

    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[:3, 3] = translation_vector

    return transformation_matrix

def transform_marker_positions(vertex_data, transformation_matrix):
    """
    Apply the transformation matrix to all marker positions.
    """
    transformed_data = {}
    for marker, positions in vertex_data.items():
        transformed_data[marker] = []
        for pos in positions:
            homogeneous_pos = np.append(pos, 1)
            transformed_pos = transformation_matrix @ homogeneous_pos
            transformed_data[marker].append(transformed_pos[:3])
    return transformed_data


def ensure_folder_exists(folder_path):
    """Create the folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def find_marker_data_folders(root_folder, target_folder_name):
    """
    Recursively search for folders that contain a subfolder with the specified name.

    :param root_folder: Root folder to search in.
    :param target_folder_name: Name of the subfolder to look for (e.g., "CameraHMR").
    :return: List of full paths of subfolders matching the target name.
    """
    matching_folders = set()
    for root, dirs, files in os.walk(root_folder):
        if target_folder_name in dirs:
            full_path = os.path.join(root, target_folder_name)
            matching_folders.add(full_path)
    return list(matching_folders)


def extract_vertex_timeseries(folder_path, initial_marker_vertices):
    """
    Extracts (x, z, y) coordinates of specified vertices from OBJ files in a folder as time-series data.

    :param folder_path: Path to the folder containing OBJ files.
    :param initial_marker_vertices: Dictionary mapping marker names to their vertex IDs.
    :return: A tuple containing:
             - marker_positions: A list of dictionaries with marker positions over time.
             - output_filename: A common substring extracted from the OBJ filenames.
    """
    obj_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.obj')])
    vertex_data = {name: [] for name in initial_marker_vertices.keys()}

    for file in obj_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.startswith('v ')]

        for name, vid in initial_marker_vertices.items():
            index = vid
            if index < len(lines):
                parts = lines[index].split()
                x, y, z = map(float, parts[1:4])
                vertex_data[name].append((x, y, z))
            else:
                print(f"Warning: Vertex ID {vid} out of range in file {file}")

    # Rotate data to have feet on the ground.
    # TODO: this does not work yet.For now the model output is not aligned with the ground. For joint angles, except the pelvis this does not matter.
    #transformation_matrix = compute_transformation_matrix(vertex_data)
    #transformed_data = transform_marker_positions(vertex_data, transformation_matrix)
    transformed_data = vertex_data

    # Assemble marker positions per frame.
    marker_positions = [
        {name: transformed_data[name][i] for name in transformed_data}
        for i in range(len(next(iter(transformed_data.values()))))
    ]

    # Create output filename based on common substring in the OBJ filenames.
    output_filename = find_common_substring(obj_files)

    return marker_positions, output_filename


def find_common_substring(strings):
    """
    Find the common substring in all entries, removing everything between the last underscore and .obj.
    """
    if not strings:
        return ""
    processed_strings = [s.rsplit('_', 1)[0] for s in strings]
    shortest = min(processed_strings, key=len)
    for length in range(len(shortest), 0, -1):
        for start in range(len(shortest) - length + 1):
            substr = shortest[start:start + length]
            if all(substr in s for s in processed_strings):
                return substr
    return ""


def save_to_trc(initial_marker_vertices, marker_positions, frame_rate, output_file):
    """
    Save the marker positions time series data to a .trc file.

    :param initial_marker_vertices: Dictionary mapping marker names to vertex IDs.
    :param marker_positions: List of dictionaries with marker positions over time.
    :param frame_rate: Frame rate for the data.
    :param output_file: Full path to the output .trc file.
    """
    num_frames = len(marker_positions)
    marker_names = list(initial_marker_vertices.keys())
    num_markers = len(marker_names)

    with open(output_file, 'w', newline='') as f:
        f.write('PathFileType\t4\t(X/Y/Z)\t{}\r\n'.format(output_file))
        f.write(
            'DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\r\n')
        f.write(
            f'{frame_rate:.6f}\t{frame_rate:.6f}\t{num_frames}\t{num_markers}\tm\t{frame_rate:.6f}\t1\t{num_frames}\r\n')
        f.write('Frame#\tTime\t')
        for name in marker_names:
            f.write(f'{name}\t\t\t')
        f.write('\r\n')

        f.write('\t\t')
        for i in range(1, num_markers + 1):
            f.write(f'X{i}\tY{i}\tZ{i}\t')
        f.write('\r\n')

        for frame_idx, frame_markers in enumerate(marker_positions):
            time = frame_idx / frame_rate
            row = [f'{frame_idx + 1}', f'{time:.5f}']
            for name in marker_names:
                marker = frame_markers.get(name, [float("nan")] * 3)
                row.extend([f'{marker[0]:.5f}', f'{marker[1]:.5f}', f'{marker[2]:.5f}'])
            f.write('\t'.join(row) + '\r\n')

    print(f"TRC file saved to {output_file}")
